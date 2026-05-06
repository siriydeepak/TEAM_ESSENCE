"""
AetherShelf Backend — FastAPI
Household Metabolist v2 | Flux Algorithm | OpenWeatherMap | Gmail Ingestion
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
import uuid, requests
from typing import Optional, List
from pydantic import BaseModel

app = FastAPI(title="AetherShelf API", version="2.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

OWM_API_KEY = "86a9711ca833b672b3cc7cf70400535c"

# ── In-Memory Store (replace with MongoDB in production) ──────────────────────
inventory_db = [
    {"id":"1","name":"Amul Whole Milk","category":"Dairy","quantity":1.5,"unit":"L","purchase_date":"2025-05-03","expiry_date":"2025-05-07","days_left":2,"shelf_life_days":7,"status":"critical","price":62,"source":"Gmail · Blinkit"},
    {"id":"2","name":"Farm Fresh Eggs","category":"Protein","quantity":12,"unit":"pcs","purchase_date":"2025-04-28","expiry_date":"2025-05-16","days_left":8,"shelf_life_days":21,"status":"good","price":96,"source":"SMS · BigBasket"},
    {"id":"3","name":"Britannia Brown Bread","category":"Bakery","quantity":0.5,"unit":"loaf","purchase_date":"2025-05-04","expiry_date":"2025-05-06","days_left":1,"shelf_life_days":5,"status":"urgent","price":45,"source":"Gmail · Zepto"},
    {"id":"4","name":"Amul Greek Yogurt","category":"Dairy","quantity":400,"unit":"g","purchase_date":"2025-05-01","expiry_date":"2025-05-09","days_left":6,"shelf_life_days":14,"status":"warning","price":89,"source":"Manual"},
    {"id":"5","name":"Baby Spinach","category":"Vegetables","quantity":150,"unit":"g","purchase_date":"2025-05-03","expiry_date":"2025-05-05","days_left":0,"shelf_life_days":5,"status":"expired","price":35,"source":"Gmail · Swiggy"},
    {"id":"6","name":"Amul Cheddar Cheese","category":"Dairy","quantity":200,"unit":"g","purchase_date":"2025-04-25","expiry_date":"2025-05-25","days_left":18,"shelf_life_days":30,"status":"good","price":195,"source":"Manual"},
    {"id":"7","name":"Chicken Breast","category":"Protein","quantity":500,"unit":"g","purchase_date":"2025-05-01","expiry_date":"2025-05-03","days_left":-2,"shelf_life_days":3,"status":"expired","price":220,"source":"SMS · Licious"},
    {"id":"8","name":"Basmati Rice","category":"Grains","quantity":2,"unit":"kg","purchase_date":"2025-04-01","expiry_date":"2025-10-01","days_left":180,"shelf_life_days":180,"status":"good","price":299,"source":"Gmail · Amazon"},
    {"id":"9","name":"Haldiram's Mixture","category":"Snacks","quantity":1,"unit":"packet","purchase_date":"2025-04-20","expiry_date":"2025-06-20","days_left":45,"shelf_life_days":60,"status":"good","price":40,"source":"Manual"},
    {"id":"10","name":"Mother Dairy Toned Milk","category":"Dairy","quantity":0.5,"unit":"L","purchase_date":"2025-05-03","expiry_date":"2025-05-04","days_left":-1,"shelf_life_days":2,"status":"expired","price":28,"source":"Gmail · Milkbasket"},
]

gap_finder_db = [
    {"id":"g1","suggestion":"Masala Omelette","missing":"Onion, Green Chilli","have":["Eggs","Milk","Cheddar Cheese"],"confidence":94,"meals":3,"category":"breakfast","cuisine":"Indian","recipe":"Beat eggs with salt, turmeric, red chilli. Add onion, green chilli. Cook in butter till set.","image_query":"masala omelette indian"},
    {"id":"g2","suggestion":"Palak Paneer","missing":"Paneer, Garlic, Cream","have":["Baby Spinach","Onion"],"confidence":87,"meals":2,"category":"dinner","cuisine":"Indian","recipe":"Blanch spinach, blend. Sauté onion-garlic, add spices, spinach, paneer. Finish with cream.","image_query":"palak paneer restaurant"},
    {"id":"g3","suggestion":"Mango Lassi","missing":"Mango Pulp, Sugar","have":["Amul Greek Yogurt","Milk"],"confidence":96,"meals":2,"category":"beverages","cuisine":"Indian","recipe":"Blend yogurt, milk, mango pulp, sugar, cardamom. Serve chilled.","image_query":"mango lassi drink"},
    {"id":"g4","suggestion":"Rice Kheer","missing":"Sugar, Cardamom, Saffron","have":["Basmati Rice","Amul Whole Milk"],"confidence":85,"meals":6,"category":"desserts","cuisine":"Indian","recipe":"Boil milk, add soaked rice. Cook 45 min, add sugar, cardamom, saffron.","image_query":"rice kheer dessert"},
    {"id":"g5","suggestion":"Dahi Chawal","missing":"Cumin, Salt","have":["Basmati Rice","Amul Greek Yogurt"],"confidence":99,"meals":2,"category":"lunch","cuisine":"Indian","recipe":"Mix cooled rice with beaten yogurt. Season with roasted cumin and salt.","image_query":"dahi chawal curd rice"},
]

smart_cart_db = [
    {"id":"c1","name":"Oat Milk (Barista Blend)","reason":"Out of stock — used daily","urgency":"high","best_price":189,"original_price":240,"source":"Blinkit","savings_pct":21,"approved":False},
    {"id":"c2","name":"Organic Pasture Eggs","reason":"Low stock — 2 remaining","urgency":"medium","best_price":115,"original_price":150,"source":"BigBasket","savings_pct":23,"approved":False},
    {"id":"c3","name":"Britannia Bread WW","reason":"Expires tomorrow","urgency":"high","best_price":42,"original_price":55,"source":"Zepto","savings_pct":24,"approved":True},
]

expiry_logs_db = [
    {"id":"e1","item":"Baby Spinach","action":"expired_discarded","date":"2025-05-05","waste_value":35,"category":"Vegetables"},
    {"id":"e2","item":"Chicken Breast","action":"expired_discarded","date":"2025-05-05","waste_value":220,"category":"Protein"},
    {"id":"e3","item":"Amul Greek Yogurt","action":"consumed","date":"2025-05-04","waste_value":0,"category":"Dairy"},
    {"id":"e4","item":"Amul Milk 1L","action":"consumed_before_expiry","date":"2025-05-03","waste_value":0,"category":"Dairy"},
]

# ── Pydantic Models ───────────────────────────────────────────────────────────
class InventoryItem(BaseModel):
    name: str
    category: str
    quantity: float
    unit: str
    shelf_life_days: int
    price: Optional[float] = None

class ReceiptInput(BaseModel):
    content: str
    source: str = "gmail"

class CartApproval(BaseModel):
    item_id: str
    approved: bool

class LocationInput(BaseModel):
    city: str

# ── Helpers ───────────────────────────────────────────────────────────────────
def _item_status(days_left: int) -> str:
    if days_left < 0: return "expired"
    if days_left == 0: return "urgent"
    if days_left <= 1: return "urgent"
    if days_left <= 3: return "critical"
    if days_left <= 7: return "warning"
    return "good"

def _flux_penalty(temp: float, humidity: int) -> float:
    """Household Metabolist — shelf life decay multiplier."""
    penalty = 0.0
    if temp > 25:
        penalty += (temp - 25) * 0.08           # 8% per °C above 25
    if humidity > 60:
        penalty += ((humidity - 60) // 5) * 0.03  # 3% per 5% humidity above 60
    return min(penalty, 0.60)                   # cap at 60%

# ── Routes ─────────────────────────────────────────────────────────────────────
@app.get("/")
def root():
    return {"message": "AetherShelf API v2.0", "status": "operational"}

@app.get("/api/inventory")
def get_inventory():
    return {"items": inventory_db, "total": len(inventory_db)}

@app.get("/api/inventory/expiring")
def get_expiring(days: int = 3):
    items = [i for i in inventory_db if i.get("days_left") is not None and 0 <= i["days_left"] <= days]
    return {"items": sorted(items, key=lambda x: x["days_left"]), "count": len(items)}

@app.get("/api/inventory/expired")
def get_expired():
    items = [i for i in inventory_db if i.get("days_left") is not None and i["days_left"] < 0]
    return {"items": items, "count": len(items)}

@app.post("/api/inventory/add")
def add_item(item: InventoryItem):
    today = datetime.now()
    expiry = today + timedelta(days=item.shelf_life_days)
    new_item = {
        "id": str(uuid.uuid4())[:8],
        "name": item.name, "category": item.category,
        "quantity": item.quantity, "unit": item.unit,
        "purchase_date": today.strftime("%Y-%m-%d"),
        "expiry_date": expiry.strftime("%Y-%m-%d"),
        "days_left": item.shelf_life_days,
        "shelf_life_days": item.shelf_life_days,
        "status": _item_status(item.shelf_life_days),
        "price": item.price, "source": "Manual"
    }
    inventory_db.append(new_item)
    return {"message": "Item added", "item": new_item}

# ── Weather — Two-Step: Geocoding → Current Weather ───────────────────────────
@app.post("/api/weather/location")
def get_weather_by_city(loc: LocationInput):
    """
    Step A: Geocoding (city → lat/lon)
    Step B: Weather retrieval (lat/lon → temp + humidity)
    Step C: Apply Flux Algorithm to inventory
    """
    # Step A
    geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={loc.city}&limit=1&appid={OWM_API_KEY}"
    geo_data = requests.get(geo_url, timeout=5).json()
    if not geo_data:
        raise HTTPException(status_code=404, detail="City not found")
    lat, lon = geo_data[0]["lat"], geo_data[0]["lon"]
    city_name = f"{geo_data[0]['name']}, {geo_data[0].get('country','')}"

    # Step B
    weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OWM_API_KEY}&units=metric"
    w = requests.get(weather_url, timeout=5).json()
    temp = round(w["main"]["temp"], 1)
    humidity = w["main"]["humidity"]
    description = w["weather"][0]["description"]

    # Step C — Flux Algorithm
    penalty = _flux_penalty(temp, humidity)
    perishable = ["Dairy", "Protein", "Vegetables", "Bakery"]
    adjustments = []
    for item in inventory_db:
        if item["category"] in perishable and item.get("days_left") and item["days_left"] > 0:
            orig = item["days_left"]
            item["days_left"] = max(0, int(orig * (1 - penalty)))
            item["status"] = _item_status(item["days_left"])
            if item["days_left"] < orig:
                adjustments.append({"item": item["name"], "original_days": orig, "adjusted_days": item["days_left"]})

    return {
        "city": city_name, "lat": lat, "lon": lon,
        "temperature_celsius": temp, "humidity": humidity,
        "description": description,
        "flux_penalty_pct": round(penalty * 100, 1),
        "alert": temp > 28 or humidity > 70,
        "adjustments": adjustments
    }

@app.get("/api/weather/shelf-impact")
def weather_shelf_impact_legacy():
    """Legacy endpoint — returns mock weather data for offline mode."""
    import random
    temp = round(30 + random.uniform(0, 8), 1)
    humidity = random.randint(65, 88)
    penalty = _flux_penalty(temp, humidity)
    return {
        "temperature_celsius": temp, "humidity": humidity,
        "alert": True, "flux_penalty_pct": round(penalty * 100, 1),
        "message": f"⚠️ {temp}°C · {humidity}% humidity — shelf lives reduced by {round(penalty*100)}%",
        "adjustments": [
            {"item": "Amul Whole Milk", "original_days": 4, "adjusted_days": max(0, int(4*(1-penalty)))},
            {"item": "Baby Spinach", "original_days": 3, "adjusted_days": max(0, int(3*(1-penalty)))},
        ]
    }

# ── Gap Finder ────────────────────────────────────────────────────────────────
@app.get("/api/gap-finder")
def get_gap_finder():
    return {"suggestions": gap_finder_db}

# ── Smart Cart ────────────────────────────────────────────────────────────────
@app.get("/api/smart-cart")
def get_smart_cart():
    total_savings = sum((i["original_price"] - i["best_price"]) for i in smart_cart_db)
    return {"items": smart_cart_db, "total_savings": round(total_savings, 2),
            "pending_count": len([i for i in smart_cart_db if not i["approved"]])}

@app.post("/api/smart-cart/approve")
def approve_cart_item(approval: CartApproval):
    for item in smart_cart_db:
        if item["id"] == approval.item_id:
            item["approved"] = approval.approved
            return {"message": "Updated", "item": item}
    raise HTTPException(status_code=404, detail="Item not found")

# ── Receipt Ingestion (Gmail parser integration) ──────────────────────────────
@app.post("/api/ingest/receipt")
async def ingest_receipt(receipt: ReceiptInput):
    """
    Mirrors the Gmail parsing logic from index.js (TEAM_ESSENCE).
    Detects platform (Blinkit / Zepto / Amazon / BigBasket / Swiggy),
    extracts items, runs collision detection against active inventory.
    """
    text = receipt.content
    platform = (
        "Blinkit" if "blinkit" in text.lower() else
        "Zepto" if "zepto" in text.lower() else
        "Amazon Fresh" if "amazon" in text.lower() else
        "BigBasket" if "bigbasket" in text.lower() else
        "Swiggy Instamart" if "swiggy" in text.lower() else
        "Unknown"
    )

    import re
    lines = [l.strip() for l in text.split('\n') if re.search(r'₹|Rs\.|[-•]', l)]
    extracted = []
    for line in lines[:10]:
        name_m = re.search(r'[-•*]\s*([A-Za-z\s]+?)(?:\s+x?\d|\s+₹|$)', line)
        qty_m = re.search(r'x(\d+)', line, re.IGNORECASE)
        price_m = re.search(r'(?:₹|Rs\.?)\s*(\d+(?:\.\d+)?)', line)
        if name_m:
            extracted.append({
                "name": name_m.group(1).strip(),
                "quantity": int(qty_m.group(1)) if qty_m else 1,
                "price_inr": float(price_m.group(1)) if price_m else None
            })

    # Collision detection (mirrors main.py check_collision)
    collisions = []
    for new_item in extracted:
        keyword = new_item["name"].lower().split()[0]
        existing = next((i for i in inventory_db if keyword in i["name"].lower() and i.get("days_left", 99) >= 0), None)
        if existing and existing.get("days_left", 99) <= 5:
            collisions.append(f"Collision! You have {existing['name']} expiring in {existing['days_left']}d — do you need more?")

    return {
        "status": "ingested", "platform": platform, "source": receipt.source,
        "extracted_items": extracted, "collision_alerts": collisions,
        "message": f"Extracted {len(extracted)} items from {platform}"
    }

# ── Expiry Logs ────────────────────────────────────────────────────────────────
@app.get("/api/expiry-logs")
def get_expiry_logs():
    total_waste = sum(i["waste_value"] for i in expiry_logs_db)
    return {"logs": expiry_logs_db, "total_waste_value_inr": round(total_waste, 2)}

# ── Analytics ──────────────────────────────────────────────────────────────────
@app.get("/api/analytics/summary")
def get_analytics():
    expiring_soon = len([i for i in inventory_db if i.get("days_left") is not None and 0 <= i["days_left"] <= 3])
    expired = len([i for i in inventory_db if i.get("days_left") is not None and i["days_left"] < 0])
    healthy = len([i for i in inventory_db if i.get("days_left") is not None and i["days_left"] > 7])
    total_waste_inr = sum(i["waste_value"] for i in expiry_logs_db)
    score = max(0, min(100, 100 - expired*20 - expiring_soon*8))
    return {
        "total_items": len(inventory_db),
        "expiring_soon": expiring_soon,
        "expired": expired, "healthy": healthy,
        "freshness_score": score,
        "total_waste_inr": round(total_waste_inr, 2),
        "smart_cart_savings_inr": sum((i["original_price"]-i["best_price"]) for i in smart_cart_db)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
