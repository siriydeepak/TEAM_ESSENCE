import os
import sys
import json
import time
import datetime
import asyncio
import threading
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml
import uvicorn
from fastapi import FastAPI, HTTPException, Request, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from dotenv import load_dotenv

# ─────────────────────────────────────────────────────────────────────────────
#  OpenClaw Framework Bootstrap
# ─────────────────────────────────────────────────────────────────────────────
load_dotenv()
ROOT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT_DIR))

import ledger_handler
from flux_engine import parse_expiry, get_decay_days, calculate_days_remaining, TODAY

# ─────────────────────────────────────────────────────────────────────────────
#  Logging — dual sink: file (streamed to UI) + console
# ─────────────────────────────────────────────────────────────────────────────
LOG_PATH = ROOT_DIR / "openclaw_session.log"

# Force UTF-8 on stdout so emoji/box-drawing chars don't crash Windows cp1252 terminals
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [OpenClaw] %(message)s",
    handlers=[
        logging.FileHandler(LOG_PATH, encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
log = logging.getLogger("sentinel")


# ─────────────────────────────────────────────────────────────────────────────
#  Environment / Config
# ─────────────────────────────────────────────────────────────────────────────
PORT = int(os.getenv("DASHBOARD_PORT", "8000"))
API_KEY = os.getenv("AETHERSHELF_CLOUD_API_KEY", "secure_claw_live_demo_123")
VAPID_PUBLIC_KEY = os.getenv("VAPID_PUBLIC_KEY", "")
VAPID_PRIVATE_KEY = os.getenv("VAPID_PRIVATE_KEY", "")
VAPID_SUBJECT = os.getenv("VAPID_SUBJECT", "mailto:sentinel@aethershelf.app")

# In-memory push subscription store  {endpoint: subscription_info_dict}
push_subscriptions: Dict[str, dict] = {}

# ─────────────────────────────────────────────────────────────────────────────
#  FastAPI App
# ─────────────────────────────────────────────────────────────────────────────
app = FastAPI(title="AetherShelf Sentinel — OpenClaw Brain (Bengaluru Node)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve the mobile PWA from /public
PUBLIC_DIR = ROOT_DIR / "public"
PUBLIC_DIR.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory=str(PUBLIC_DIR)), name="static")


# ─────────────────────────────────────────────────────────────────────────────
#  Pydantic Models
# ─────────────────────────────────────────────────────────────────────────────
class PushSubscription(BaseModel):
    endpoint: str
    keys: Dict[str, str]  # {"p256dh": ..., "auth": ...}

class InventoryUpdate(BaseModel):
    item_name: str
    quantity: int
    estimated_expiry: Optional[str] = None

class SyncData(BaseModel):
    ledger: list


# ─────────────────────────────────────────────────────────────────────────────
#  OpenClaw Action-Observation Loop  (runs in background thread)
# ─────────────────────────────────────────────────────────────────────────────

LEDGER_PATH = ROOT_DIR / "pantry_ledger.yaml"

def _send_web_push(subscription_info: dict, payload: dict) -> bool:
    """
    Fire a Web Push notification using pywebpush.
    Falls back gracefully if pywebpush is not installed.
    """
    try:
        from pywebpush import webpush, WebPushException  # type: ignore
        webpush(
            subscription_info=subscription_info,
            data=json.dumps(payload),
            vapid_private_key=VAPID_PRIVATE_KEY,
            vapid_claims={"sub": VAPID_SUBJECT},
        )
        return True
    except ImportError:
        log.warning("[OpenClaw] pywebpush not installed — push skipped. Run: pip install pywebpush")
        return False
    except Exception as exc:
        log.error(f"[OpenClaw] Push delivery error: {exc}")
        return False


def _broadcast_push(title: str, body: str, urgency: str = "high", tag: str = "sentinel"):
    """Deliver a push notification to ALL registered subscribers."""
    if not VAPID_PRIVATE_KEY:
        log.warning("[OpenClaw] VAPID keys not configured. Run generate_vapid_keys.py first.")
        return

    payload = {
        "title": title,
        "body": body,
        "tag": tag,
        "urgency": urgency,
        "icon": "/icon-192.png",
        "badge": "/icon-96.png",
    }

    stale = []
    for endpoint, sub in list(push_subscriptions.items()):
        ok = _send_web_push(sub, payload)
        if not ok:
            stale.append(endpoint)

    for ep in stale:
        push_subscriptions.pop(ep, None)

    log.info(f"[OpenClaw] Push dispatched → '{title}' to {len(push_subscriptions)} subscriber(s).")


def openclaw_action_observation_loop():
    """
    OpenClaw Autonomous Brain — Action-Observation Loop.

    Observation Phase:
        Watches pantry_ledger.yaml for file-system changes (mtime polling).

    Reasoning Phase (FluxAlgorithm.skill):
        Calculates per-item days-remaining and pantry-wide entropy.

    Action Phase:
        • Critical Entropy  → Web Push notification (expiry ≤ 24 h)
        • Inventory Depletion → Web Push notification (quantity == 0)
        • Collision Detection → logged & pushed
        • UtilityGapFinder  → suggestion push

    The loop writes structured chain-of-thought to openclaw_session.log
    for the live terminal on the mobile UI.
    """
    log.info("╔══════════════════════════════════════════════════════╗")
    log.info("║  AetherShelf Sentinel — OpenClaw Action-Obs. Loop   ║")
    log.info("║  Monitoring: pantry_ledger.yaml  |  Node: Bengaluru  ║")
    log.info("╚══════════════════════════════════════════════════════╝")

    last_mtime: float = 0.0
    loop_count: int = 0

    while True:
        try:
            current_mtime = LEDGER_PATH.stat().st_mtime if LEDGER_PATH.exists() else last_mtime
        except OSError:
            current_mtime = last_mtime

        if current_mtime != last_mtime:
            last_mtime = current_mtime
            loop_count += 1

            # ── OBSERVATION ──────────────────────────────────────────────────
            log.info(f"[Observe #{loop_count}] Ledger change detected. Loading snapshot...")
            items = ledger_handler.load_ledger(LEDGER_PATH)
            log.info(f"[Observe #{loop_count}] {len(items)} item(s) ingested from pantry_ledger.yaml")

            # ── REASONING (FluxAlgorithm.skill) ──────────────────────────────
            log.info("[Reason] FluxAlgorithm.skill → calculating entropy for each item...")
            total_days = 0
            item_count = len(items)
            critical_items = []      # ≤ 1 day
            depleted_items = []      # qty == 0
            low_items = []           # ≤ 3 days

            for item in items:
                name = str(item.get("name", "Unknown"))
                qty = int(item.get("quantity", 0))

                expiry_date = parse_expiry(item.get("estimated_expiry"))
                if expiry_date is None:
                    decay = get_decay_days(name)
                    expiry_date = TODAY + datetime.timedelta(days=decay)

                days = calculate_days_remaining(expiry_date)
                total_days += max(days, 0)

                log.info(f"  · {name:<30} qty={qty:<4} days_remaining={days}")

                if qty == 0:
                    depleted_items.append(name)
                elif days <= 1:
                    critical_items.append((name, days))
                elif days <= 3:
                    low_items.append((name, days))

            pantry_entropy = total_days / item_count if item_count else 0.0
            log.info(f"[Reason] Pantry Entropy Score = {pantry_entropy:.2f} days (avg freshness)")

            # ── ACTION PHASE ─────────────────────────────────────────────────
            # Action 1: Critical Entropy → immediate push
            for name, days in critical_items:
                hours_left = days * 24
                log.info(f"[Action] CRITICAL ENTROPY  → {name} expires in ~{hours_left}h — triggering Web Push")
                _broadcast_push(
                    title="🚨 Agent Alert: Critical Expiry!",
                    body=f"{name} expires in {hours_left} hours. Consume or discard immediately.",
                    urgency="high",
                    tag=f"critical_{name.lower().replace(' ', '_')}",
                )

            # Action 2: Inventory Depletion → restock push
            for name in depleted_items:
                log.info(f"[Action] INVENTORY DEPLETION → {name} at zero — triggering Restock Push")
                _broadcast_push(
                    title="📦 Restock Alert",
                    body=f"{name} is fully depleted. FluxAlgorithm recommends restocking.",
                    urgency="normal",
                    tag=f"depleted_{name.lower().replace(' ', '_')}",
                )

            # Action 3: Low items → advisory push (batched)
            if low_items and not critical_items:
                names_str = ", ".join(f"{n} ({d}d)" for n, d in low_items)
                log.info(f"[Action] LOW STOCK ADVISORY → {names_str}")
                _broadcast_push(
                    title="⚠️ Low Stock Advisory",
                    body=f"Items running low: {names_str}. Plan restocking.",
                    urgency="normal",
                    tag="low_stock",
                )

            # Action 4: CollisionDetection.skill
            log.info("[Reason] CollisionDetection.skill → scanning for buy-collision anomalies...")
            for item in items:
                name = str(item.get("name", ""))
                qty = int(item.get("quantity", 0))
                expiry_date = parse_expiry(item.get("estimated_expiry"))
                if expiry_date and qty > 1:
                    days = calculate_days_remaining(expiry_date)
                    if 0 < days <= 3:
                        log.info(f"  [CollisionDetection] {name}: qty={qty}, days={days} → potential buy-collision")

            # Action 5: UtilityGapFinder.skill
            log.info("[Reason] UtilityGapFinder.skill → scanning for recipe-unlock opportunities...")
            names_lower = [str(i.get("name","")).lower() for i in items if int(i.get("quantity",0)) > 0]
            if any("spinach" in n for n in names_lower):
                log.info("  [UtilityGapFinder] Spinach detected → cream + garlic unlock 'Creamed Spinach' recipe")
            if any("milk" in n for n in names_lower) and any("bread" in n for n in names_lower):
                log.info("  [UtilityGapFinder] Milk + Bread → French Toast recipe opportunity detected")

            log.info(f"[Cycle #{loop_count}] Complete. Next observation on file change.")
            log.info("─" * 60)

        time.sleep(1)


# Start the OpenClaw loop in a background daemon thread
_loop_thread = threading.Thread(target=openclaw_action_observation_loop, daemon=True, name="OpenClaw-Brain")
_loop_thread.start()


# ─────────────────────────────────────────────────────────────────────────────
#  API Routes
# ─────────────────────────────────────────────────────────────────────────────

@app.post("/api/push/subscribe")
async def subscribe_push(sub: PushSubscription):
    """Register a mobile client for Web Push notifications."""
    push_subscriptions[sub.endpoint] = {
        "endpoint": sub.endpoint,
        "keys": sub.keys,
    }
    log.info(f"[Push] New subscriber registered: ...{sub.endpoint[-40:]}")
    return {"status": "subscribed", "total_subscribers": len(push_subscriptions)}


@app.delete("/api/push/subscribe")
async def unsubscribe_push(sub: PushSubscription):
    """Remove a push subscription."""
    push_subscriptions.pop(sub.endpoint, None)
    return {"status": "unsubscribed"}


@app.get("/api/push/vapid-public-key")
async def get_vapid_public_key():
    """Serve the VAPID public key to the PWA for push registration."""
    return {"vapid_public_key": VAPID_PUBLIC_KEY}


@app.post("/api/push/test")
async def test_push(background_tasks: BackgroundTasks):
    """Send a manual test push to all subscribers (demo / hackathon use)."""
    background_tasks.add_task(
        _broadcast_push,
        title="✅ Sentinel Test Push",
        body="OpenClaw brain is live and connected to your mobile device!",
        urgency="normal",
        tag="test_push",
    )
    return {"status": "push_queued", "subscribers": len(push_subscriptions)}


@app.get("/api/state")
async def get_state():
    """Full dashboard state: ledger + entropy + logs + alerts."""
    items = ledger_handler.load_ledger(LEDGER_PATH)
    formatted = []
    alerts = []

    for item in items:
        name = str(item.get("name", "Unknown"))
        qty = int(item.get("quantity", 0))
        expiry_date = parse_expiry(item.get("estimated_expiry"))

        if not expiry_date:
            decay = get_decay_days(name)
            expiry_date = TODAY + datetime.timedelta(days=decay)

        days = calculate_days_remaining(expiry_date)
        formatted.append({"name": name, "quantity": qty, "days": days, "expiry": str(expiry_date)})

        if qty == 0:
            alerts.append({"id": f"{name}_depleted", "type": "depleted", "item": name,
                            "message": f"📦 {name} is fully depleted. Restock recommended."})
        elif days <= 1:
            alerts.append({"id": f"{name}_critical", "type": "critical", "item": name,
                            "message": f"🚨 {name} expires in {days * 24:.0f}h! Critical Entropy detected."})
        elif days <= 3:
            alerts.append({"id": f"{name}_low", "type": "low", "item": name,
                            "message": f"⚠️ {name} expires in {days} day(s). Schedule restock."})

    # Logs
    logs = "Awaiting OpenClaw session..."
    if LOG_PATH.exists():
        lines = LOG_PATH.read_text(encoding="utf-8", errors="replace").splitlines()
        logs = "\n".join(lines[-80:])

    total_entropy = sum(max(i["days"], 0) for i in formatted)
    entropy_score = total_entropy / len(formatted) if formatted else 0.0

    return {
        "ledger": formatted,
        "alerts": alerts,
        "logs": logs,
        "entropy_score": round(entropy_score, 2),
        "subscriber_count": len(push_subscriptions),
        "status": "active",
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
    }


@app.get("/api/ledger")
async def get_ledger():
    """Raw ledger endpoint."""
    items = ledger_handler.load_ledger(LEDGER_PATH)
    return {"ledger": items, "status": "active"}


@app.post("/api/update-inventory")
async def update_inventory(update: InventoryUpdate):
    """Add or update a pantry item."""
    result = ledger_handler.add_item(
        update.item_name, update.quantity, update.estimated_expiry, LEDGER_PATH
    )
    log.info(f"[SecureClaw] Inventory updated via API: {update.item_name} × {update.quantity}")
    return {"status": "success", "result": result}


@app.post("/api/update")
async def cloud_sync(request: Request, data: SyncData):
    """SecureClaw authenticated cloud sync webhook."""
    auth = request.headers.get("Authorization", "")
    if auth != f"Bearer {API_KEY}":
        raise HTTPException(status_code=401, detail="SecureClaw: Unauthorized")
    # Write synced ledger to disk so the observation loop picks it up
    with open(LEDGER_PATH, "w", encoding="utf-8") as f:
        yaml.dump(data.ledger, f, allow_unicode=True)
    log.info(f"[SecureClaw] Cloud sync received: {len(data.ledger)} items written to ledger.")
    return {"status": "synced"}


@app.get("/api/pantry")
async def get_pantry():
    """
    Plotly-ready pantry endpoint.
    Returns items with freshness decay series for the next 8 days.
    """
    items = ledger_handler.load_ledger(LEDGER_PATH)
    today = datetime.date.today()
    dates = [(today + datetime.timedelta(days=i)).isoformat() for i in range(8)]

    plotly_traces = []
    table_rows = []

    for item in items:
        name = str(item.get("name", "Unknown"))
        qty  = int(item.get("quantity", 0))
        expiry_date = parse_expiry(item.get("estimated_expiry"))
        if expiry_date is None:
            expiry_date = today + datetime.timedelta(days=get_decay_days(name))

        days_left = (expiry_date - today).days
        y_vals = [max(0, days_left - i) for i in range(8)]

        plotly_traces.append({
            "name": name,
            "x": dates,
            "y": y_vals,
            "mode": "lines+markers",
            "line": {"width": 2},
            "marker": {"size": 5},
        })

        table_rows.append({
            "name": name,
            "quantity": qty,
            "days": days_left,
            "expiry": expiry_date.isoformat(),
            "status": "critical" if days_left <= 1 else "low" if days_left <= 3 else "ok",
        })

    return {
        "traces": plotly_traces,
        "table": table_rows,
        "dates": dates,
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
    }


@app.post("/api/trigger-demo")
async def trigger_demo(background_tasks: BackgroundTasks):
    """Simulate a Critical Entropy event for hackathon demonstration."""
    def _demo():
        log.info("[DEMO] ⚡ OpenClaw Autonomous Loop — DEMO MODE ACTIVATED")
        log.info("[DEMO] Simulating Critical Entropy detection on 'Milk Blinkit'...")
        time.sleep(0.5)
        log.info("[DEMO] FluxAlgorithm.skill → days_remaining = 0.5 → CRITICAL THRESHOLD BREACHED")
        time.sleep(0.5)
        log.info("[DEMO] CollisionDetection.skill → No pending purchase found")
        time.sleep(0.5)
        log.info("[DEMO] UtilityGapFinder.skill → Milk + Cereal → 'Breakfast Bowl' recipe unlocked")
        time.sleep(0.5)
        log.info("[DEMO] Triggering Web Push notification to all mobile subscribers...")
        _broadcast_push(
            title="🤖 OpenClaw Demo Alert",
            body="Milk Blinkit expires in 12h! FluxAlgorithm detected Critical Entropy. Add to cart?",
            urgency="high",
            tag="demo_alert",
        )
        log.info("[DEMO] ✅ Full Autonomous Loop cycle complete.")

    background_tasks.add_task(_demo)
    return {"status": "demo_triggered"}


# ─────────────────────────────────────────────────────────────────────────────
#  Serve PWA index.html at root
# ─────────────────────────────────────────────────────────────────────────────
from fastapi.responses import FileResponse

@app.get("/")
async def serve_pwa():
    index = PUBLIC_DIR / "index.html"
    if index.exists():
        return FileResponse(str(index), media_type="text/html")
    return JSONResponse({"error": "PWA not built. Run the project setup."}, status_code=404)

@app.get("/{filename:path}")
async def serve_static(filename: str):
    """Catch-all for PWA assets (sw.js, manifest.json, icons)."""
    target = PUBLIC_DIR / filename
    if target.exists() and target.is_file():
        return FileResponse(str(target))
    # SPA fallback
    index = PUBLIC_DIR / "index.html"
    if index.exists():
        return FileResponse(str(index), media_type="text/html")
    raise HTTPException(status_code=404, detail="Not found")


# ─────────────────────────────────────────────────────────────────────────────
#  Entry point
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    log.info(f"🚀 AetherShelf Sentinel starting on http://0.0.0.0:{PORT}")
    log.info(f"   VAPID configured: {'✅ Yes' if VAPID_PRIVATE_KEY else '❌ No — run generate_vapid_keys.py'}")
    log.info(f"   OpenClaw Brain thread: {'✅ Running' if _loop_thread.is_alive() else '❌ Dead'}")
    # Pass the app *object* directly — do NOT use 'main:app' string here.
    # Using the string causes uvicorn to re-import the module which would
    # spawn a second OpenClaw thread and lose the original push_subscriptions dict.
    uvicorn.run(app, host="0.0.0.0", port=PORT, reload=False)
