"""
╔══════════════════════════════════════════════════════════════════════════════╗
║           AetherShelf — automation_engine.py                               ║
║           Household Metabolist Flux Algorithm                               ║
║           Run every 4 hours via APScheduler / cron / GitHub Actions        ║
╚══════════════════════════════════════════════════════════════════════════════╝

MongoDB Collections:
  users       — location (lat/lon), settings
  inventory   — products with baseExpiryDate
  flux_logs   — weather snapshots + adjustedDaysLeft (analytics engine)

Inputs:  Active inventory from MongoDB + OpenWeatherMap API (temp + humidity)
Outputs: Updated flux_logs, adjustedDaysLeft, "Pantry Collision" alert JSONs

Logic:
  Temp > 25°C  → reduces shelf life 8% per degree above 25
  Humidity > 60% → reduces shelf life 3% per 5% increase above 60

Usage:
  python automation_engine.py                  # run once
  python automation_engine.py --scheduler      # run every 4 hours with APScheduler
"""

import os
import sys
import json
import logging
import argparse
from datetime import datetime, timezone
from typing import Optional

import requests
from pymongo import MongoClient, UpdateOne
from pymongo.errors import ConnectionFailure

# ── Try importing APScheduler (optional) ──────────────────────────────────────
try:
    from apscheduler.schedulers.blocking import BlockingScheduler
    HAS_SCHEDULER = True
except ImportError:
    HAS_SCHEDULER = False

# ── Logging ───────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  [%(levelname)s]  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
log = logging.getLogger("AetherShelf.AutoEngine")

# ── Config ────────────────────────────────────────────────────────────────────
OWM_API_KEY   = os.getenv("OWM_API_KEY",   "86a9711ca833b672b3cc7cf70400535c")
MONGO_URI     = os.getenv("MONGO_URI",     "mongodb://localhost:27017")
DB_NAME       = os.getenv("AETHERSHELF_DB","aethershelf")
ALERT_WEBHOOK = os.getenv("ALERT_WEBHOOK", "")   # optional: Slack / ntfy.sh URL

# Perishable categories that respond to weather
PERISHABLE_CATS = {"Dairy", "Protein", "Vegetables", "Bakery", "Fruits"}

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  MongoDB Schema (for reference — auto-created on first write)              ║
# ╚══════════════════════════════════════════════════════════════════════════════╝
#
# Collection: users
# {
#   "_id": "user_123",
#   "name": "Jane Doe",
#   "location": { "lat": 13.0827, "lon": 80.2707, "city": "Chennai" },
#   "settings": { "unit": "metric" }
# }
#
# Collection: inventory
# {
#   "_id": "item_888",
#   "userId": "user_123",
#   "productName": "Amul Whole Milk",
#   "category": "Dairy",
#   "purchaseDate": "2026-05-01T10:00:00Z",
#   "baseExpiryDate": "2026-05-07T10:00:00Z",
#   "quantity": 1,
#   "unit": "L",
#   "priceINR": 62,
#   "status": "Active"          # Active | Consumed | Expired | Discarded
# }
#
# Collection: flux_logs  (analytics engine)
# {
#   "_id": "log_999",
#   "itemId": "item_888",
#   "timestamp": "2026-05-05T15:00:00Z",
#   "environmentalFactors": { "temp": 32.5, "humidity": 82 },
#   "adjustedDaysLeft": 1.5,
#   "penaltyApplied": 0.40,
#   "isCritical": true
# }


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  Two-Step Weather: Geocoding → Current Weather                             ║
# ╚══════════════════════════════════════════════════════════════════════════════╝
def fetch_weather(lat: float, lon: float) -> dict:
    """
    Step B: Given coordinates, fetch temperature (°C) and humidity (%) 
    from the OpenWeatherMap Current Weather API.
    """
    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?lat={lat}&lon={lon}&appid={OWM_API_KEY}&units=metric"
    )
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        return {
            "temp":     round(data["main"]["temp"], 1),
            "humidity": data["main"]["humidity"],
            "desc":     data["weather"][0]["description"],
            "city":     data.get("name", ""),
        }
    except Exception as exc:
        log.error(f"OpenWeatherMap error for ({lat},{lon}): {exc}")
        return {"temp": 30.0, "humidity": 75, "desc": "simulated", "city": "unknown"}


def geocode_city(city: str) -> Optional[dict]:
    """
    Step A: Convert city name → lat/lon using the OpenWeatherMap Geocoding API.
    Called once when a user sets their location.
    """
    url = (
        f"http://api.openweathermap.org/geo/1.0/direct"
        f"?q={city}&limit=1&appid={OWM_API_KEY}"
    )
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        if data:
            return {"lat": data[0]["lat"], "lon": data[0]["lon"], "city": data[0]["name"]}
    except Exception as exc:
        log.error(f"Geocoding error for '{city}': {exc}")
    return None


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  Household Metabolist — Flux Algorithm                                     ║
# ╚══════════════════════════════════════════════════════════════════════════════╝
def calc_decay_multiplier(temp: float, humidity: int) -> float:
    """
    Shelf Life Decay Multiplier:
      • Temp > 25°C  → −8% per degree above 25
      • Humidity > 60% → −3% per 5% increase above 60
    Returns the penalty fraction (0.0 – 0.60).
    """
    penalty = 0.0
    if temp > 25:
        penalty += (temp - 25) * 0.08
    if humidity > 60:
        penalty += (int((humidity - 60) / 5)) * 0.03
    return round(min(penalty, 0.60), 4)


def calc_adjusted_days(base_expiry: datetime, penalty: float) -> float:
    """
    Given the base expiry date and a weather penalty, compute how many
    days are actually left after environmental adjustment.
    """
    now = datetime.now(timezone.utc)
    base_days_left = (base_expiry - now).total_seconds() / 86400
    if base_days_left <= 0:
        return 0.0
    return round(base_days_left * (1 - penalty), 2)


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  Pantry Collision Alert                                                    ║
# ╚══════════════════════════════════════════════════════════════════════════════╝
def build_collision_alert(item: dict, adjusted_days: float) -> dict:
    """Generate a Pantry Collision alert JSON for critical items."""
    return {
        "alert_type":    "PANTRY_COLLISION",
        "timestamp":     datetime.now(timezone.utc).isoformat(),
        "item_id":       str(item["_id"]),
        "product_name":  item.get("productName", "Unknown"),
        "category":      item.get("category", ""),
        "adjusted_days_left": adjusted_days,
        "message": (
            f"⚠ CRITICAL: {item.get('productName')} will spoil in "
            f"{adjusted_days:.1f} day(s) due to current weather conditions. "
            f"Use it today!"
        ),
        "recommended_action": "consume_immediately" if adjusted_days < 0.5 else "consume_today"
    }


def push_alert(alert: dict):
    """
    Push a Pantry Collision alert to a webhook (Slack / ntfy.sh / Firebase).
    Extend this to use WebSockets or FCM for the React frontend.
    """
    if ALERT_WEBHOOK:
        try:
            requests.post(ALERT_WEBHOOK, json=alert, timeout=5)
            log.info(f"Alert pushed: {alert['product_name']}")
        except Exception as exc:
            log.warning(f"Alert webhook failed: {exc}")
    else:
        # Print to stdout — can be piped to any notification system
        print(json.dumps(alert, indent=2))


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  Main Flux Run                                                             ║
# ╚══════════════════════════════════════════════════════════════════════════════╝
def run_flux_engine(db):
    """
    Core automation loop:
      1. Pull all unique user locations from MongoDB.
      2. Fetch weather for each location (one API call per location, not per item).
      3. Iterate active inventory for that user.
      4. Apply Flux Algorithm → update flux_logs.
      5. If adjustedDaysLeft < 1 → generate Pantry Collision alert.
    """
    log.info("═══ AetherShelf Flux Engine Starting ═══")
    users      = db["users"]
    inventory  = db["inventory"]
    flux_logs  = db["flux_logs"]

    # Fetch all unique locations in one pass
    weather_cache: dict[str, dict] = {}

    all_users = list(users.find({}))
    if not all_users:
        log.warning("No users found in MongoDB — add users first.")
        return

    collision_alerts = []
    flux_ops = []

    for user in all_users:
        loc  = user.get("location", {})
        lat  = loc.get("lat")
        lon  = loc.get("lon")
        city = loc.get("city", "Unknown")
        uid  = str(user["_id"])

        if lat is None or lon is None:
            log.warning(f"User {uid} has no location coordinates — skipping.")
            continue

        # Cache weather per unique lat/lon pair (avoid duplicate API calls)
        cache_key = f"{lat:.4f},{lon:.4f}"
        if cache_key not in weather_cache:
            log.info(f"Fetching weather for {city} ({lat}, {lon}) …")
            weather_cache[cache_key] = fetch_weather(lat, lon)
        weather = weather_cache[cache_key]

        temp     = weather["temp"]
        humidity = weather["humidity"]
        penalty  = calc_decay_multiplier(temp, humidity)

        log.info(
            f"User {uid} | {city} | {temp}°C · {humidity}% humidity | "
            f"Penalty: -{penalty*100:.1f}%"
        )

        # Process active inventory items for this user
        active_items = list(inventory.find({
            "userId": uid,
            "status": "Active",
            "category": {"$in": list(PERISHABLE_CATS)}
        }))

        log.info(f"  → {len(active_items)} perishable items to process")

        for item in active_items:
            base_expiry_raw = item.get("baseExpiryDate")
            if not base_expiry_raw:
                continue

            # Normalise to timezone-aware datetime
            if isinstance(base_expiry_raw, str):
                base_expiry = datetime.fromisoformat(base_expiry_raw.replace("Z", "+00:00"))
            else:
                base_expiry = base_expiry_raw.replace(tzinfo=timezone.utc)

            adjusted_days = calc_adjusted_days(base_expiry, penalty)
            is_critical   = adjusted_days < 1.0

            # Build the flux log document
            log_doc = {
                "itemId":    str(item["_id"]),
                "userId":    uid,
                "timestamp": datetime.now(timezone.utc).isoformat() + "Z",
                "environmentalFactors": {
                    "temp":     temp,
                    "humidity": humidity,
                    "city":     city,
                },
                "penaltyApplied":  penalty,
                "adjustedDaysLeft": adjusted_days,
                "isCritical":      is_critical,
            }
            flux_ops.append(log_doc)

            # Pantry Collision alert
            if is_critical:
                alert = build_collision_alert(item, adjusted_days)
                collision_alerts.append(alert)
                log.warning(
                    f"  ⚠  COLLISION: {item.get('productName')} → "
                    f"{adjusted_days:.1f}d left!"
                )

    # Bulk-insert all flux logs
    if flux_ops:
        result = flux_logs.insert_many(flux_ops)
        log.info(f"Inserted {len(result.inserted_ids)} flux log entries.")

    # Push alerts
    for alert in collision_alerts:
        push_alert(alert)

    log.info(
        f"═══ Run complete: {len(flux_ops)} logs | "
        f"{len(collision_alerts)} collision alerts ═══"
    )
    return {"logs_written": len(flux_ops), "alerts": collision_alerts}


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  Demo / Seed helper                                                        ║
# ╚══════════════════════════════════════════════════════════════════════════════╝
def seed_demo_data(db):
    """Insert sample user + inventory documents for testing."""
    users     = db["users"]
    inventory = db["inventory"]

    # Upsert a demo user in Chennai
    users.update_one(
        {"_id": "user_demo"},
        {"$set": {
            "_id":      "user_demo",
            "name":     "Demo User",
            "location": {"lat": 13.0827, "lon": 80.2707, "city": "Chennai"},
            "settings": {"unit": "metric"}
        }},
        upsert=True
    )

    now = datetime.now(timezone.utc)
    demo_items = [
        {"_id": "item_001", "userId": "user_demo", "productName": "Amul Whole Milk", "category": "Dairy",
         "purchaseDate": now.isoformat(), "baseExpiryDate": (now + __import__('datetime').timedelta(days=3)).isoformat(),
         "quantity": 1, "unit": "L", "priceINR": 62, "status": "Active"},
        {"_id": "item_002", "userId": "user_demo", "productName": "Baby Spinach", "category": "Vegetables",
         "purchaseDate": now.isoformat(), "baseExpiryDate": (now + __import__('datetime').timedelta(days=2)).isoformat(),
         "quantity": 150, "unit": "g", "priceINR": 35, "status": "Active"},
        {"_id": "item_003", "userId": "user_demo", "productName": "Chicken Breast", "category": "Protein",
         "purchaseDate": now.isoformat(), "baseExpiryDate": (now + __import__('datetime').timedelta(hours=18)).isoformat(),
         "quantity": 500, "unit": "g", "priceINR": 220, "status": "Active"},
    ]

    for item in demo_items:
        inventory.update_one({"_id": item["_id"]}, {"$set": item}, upsert=True)

    log.info(f"Demo data seeded: 1 user, {len(demo_items)} inventory items.")


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  Entry Point                                                               ║
# ╚══════════════════════════════════════════════════════════════════════════════╝
def main():
    parser = argparse.ArgumentParser(description="AetherShelf Automation Engine")
    parser.add_argument("--scheduler", action="store_true", help="Run every 4 hours with APScheduler")
    parser.add_argument("--seed",      action="store_true", help="Seed demo data into MongoDB first")
    parser.add_argument("--dry-run",   action="store_true", help="Run without writing to MongoDB")
    args = parser.parse_args()

    # Connect to MongoDB
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        client.server_info()  # Raises if not connected
        db = client[DB_NAME]
        log.info(f"Connected to MongoDB: {MONGO_URI} / {DB_NAME}")
    except ConnectionFailure as exc:
        log.error(f"Cannot connect to MongoDB at {MONGO_URI}: {exc}")
        log.info("To run without MongoDB, use --dry-run mode.")
        if not args.dry_run:
            sys.exit(1)
        db = None

    if args.seed and db is not None:
        seed_demo_data(db)

    if args.dry_run:
        log.info("Dry-run mode: fetching weather for Chennai only.")
        weather = fetch_weather(13.0827, 80.2707)
        penalty = calc_decay_multiplier(weather["temp"], weather["humidity"])
        print(json.dumps({
            "city": "Chennai (dry-run)",
            "weather": weather,
            "flux_penalty_pct": round(penalty * 100, 1),
            "example_item": {
                "name": "Amul Milk",
                "base_days_left": 3,
                "adjusted_days_left": round(3 * (1 - penalty), 2)
            }
        }, indent=2))
        return

    if args.scheduler:
        if not HAS_SCHEDULER:
            log.error("APScheduler not installed. Run: pip install apscheduler")
            sys.exit(1)
        scheduler = BlockingScheduler()
        scheduler.add_job(lambda: run_flux_engine(db), "interval", hours=4, id="flux_engine",
                          next_run_time=datetime.now())
        log.info("Scheduler started — running every 4 hours. Press Ctrl+C to stop.")
        try:
            scheduler.start()
        except (KeyboardInterrupt, SystemExit):
            log.info("Scheduler stopped.")
    else:
        run_flux_engine(db)


if __name__ == "__main__":
    main()
