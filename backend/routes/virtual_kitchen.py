"""
Virtual Kitchen API routes — hardened version.

POST /api/kitchen/upload-receipt  — Receipt photo → Gemini Vision (forced JSON) → pantry
POST /api/kitchen/add-item        — Manual entry → inventory + Telegram confirmation
GET  /api/kitchen/virtual-status  — Summary for a web user
"""

import os
import base64
import json
import re
import logging
from datetime import datetime, timedelta
from typing import List, Optional, Tuple

from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from pydantic import BaseModel

from ..services.telegram_service import notify_user, is_linked, get_telegram_id
from ..services.inventory_service import InventoryService
from ..models.inventory import InventoryItemCreate

logger = logging.getLogger(__name__)
router = APIRouter()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-1.5-flash:generateContent"
)

# ── System prompt — forces Gemini to return strict JSON ─────────────────────
RECEIPT_SYSTEM_PROMPT = """You are a grocery receipt OCR and item-extraction engine.
Your ONLY output must be a valid JSON array — no markdown, no code fences, no prose.

Each element must have EXACTLY these fields:
{
  "name": "string — full product name as printed",
  "quantity": number — numeric amount (default 1 if unclear),
  "unit": "string — e.g. L, kg, g, pcs, pack, bottle (default 'units')",
  "price_inr": number or null — numeric price in Indian Rupees (null if not visible),
  "category": "string — MUST be one of: Dairy, Produce, Protein, Bakery, Snacks, Beverages, Grains, Condiments, Frozen, Other"
}

Rules:
- If a field cannot be determined, use the default (quantity=1, unit="units", price_inr=null, category="Other").
- Do NOT include tax lines, totals, discounts, or store metadata.
- Output ONLY the JSON array. Any other text will break the system.
"""


class ManualItemRequest(BaseModel):
    web_user_id: str
    name: str
    quantity: float = 1.0
    unit: str = "units"
    category: str = "Other"
    price: Optional[float] = None
    shelf_life_days: int = 7


# ---------------------------------------------------------------------------
# Receipt upload
# ---------------------------------------------------------------------------

@router.post("/upload-receipt")
async def upload_receipt(
    web_user_id: str = Form(...),
    file: UploadFile = File(...),
):
    """Upload a grocery receipt image; Gemini parses it and populates the pantry."""
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image files are accepted (jpg, png, webp).")

    raw_bytes = await file.read()
    if len(raw_bytes) > 10 * 1024 * 1024:   # 10 MB guard
        raise HTTPException(status_code=413, detail="Image too large (max 10 MB).")

    b64 = base64.b64encode(raw_bytes).decode()

    # --- Gemini call ---------------------------------------------------------
    if GEMINI_API_KEY:
        extracted, parse_error = await _gemini_parse(b64, file.content_type)
    else:
        logger.warning("GEMINI_API_KEY not set — using mock items for demo.")
        extracted = _mock_items()
        parse_error = "GEMINI_API_KEY not configured — showing demo data."

    # --- Validate & persist --------------------------------------------------
    service = InventoryService()
    today = datetime.utcnow().date()
    added: List[str] = []

    for item in extracted:
        try:
            sl = _shelf_life(item.get("category", "Other"))
            await service.add_item(InventoryItemCreate(
                name=str(item["name"])[:255],
                category=str(item.get("category", "Other")),
                quantity=float(item.get("quantity") or 1),
                unit=str(item.get("unit", "units"))[:50],
                purchase_date=today,
                expiry_date=today + timedelta(days=sl),
                shelf_life_days=sl,
                price=_safe_float(item.get("price_inr")),
                source="Receipt Upload · Gemini Vision",
            ))
            added.append(item["name"])
        except Exception as exc:
            logger.error(f"Failed to persist receipt item '{item.get('name')}': {exc}")

    # --- Telegram notification -----------------------------------------------
    if added:
        lines = "\n".join(f"  • {n}" for n in added[:15])
        await notify_user(
            web_user_id,
            f"🧾 <b>Receipt processed!</b>\n\n"
            f"Added <b>{len(added)} item(s)</b> to your virtual shelf:\n{lines}"
            + (f"\n  …and {len(added)-15} more" if len(added) > 15 else ""),
        )

    return {
        "success": True,
        "parsed_items": extracted,
        "added_count": len(added),
        "added_names": added,
        "parse_error": parse_error,
        "message": f"Successfully added {len(added)} item(s) to your virtual kitchen.",
    }


async def _gemini_parse(b64: str, mime: str) -> Tuple[List[dict], Optional[str]]:
    """Call Gemini 1.5 Flash with a strict JSON-only system prompt."""
    import httpx

    payload = {
        "system_instruction": {"parts": [{"text": RECEIPT_SYSTEM_PROMPT}]},
        "contents": [{
            "parts": [
                {"text": "Extract all grocery items from this receipt image."},
                {"inline_data": {"mime_type": mime, "data": b64}},
            ]
        }],
        "generationConfig": {
            "temperature": 0.1,       # near-deterministic for structured output
            "topP": 0.9,
            "maxOutputTokens": 2048,
        },
    }

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.post(
                GEMINI_URL, params={"key": GEMINI_API_KEY}, json=payload,
            )
            r.raise_for_status()
            raw_text: str = r.json()["candidates"][0]["content"]["parts"][0]["text"]

        # Strip any stray markdown fences Gemini might still emit
        clean = re.sub(r"```(?:json)?", "", raw_text).strip().strip("`").strip()

        # Find the first '[' to '[' … ']' span — handles any leading text
        start = clean.find("[")
        end   = clean.rfind("]") + 1
        if start == -1 or end == 0:
            raise ValueError(f"No JSON array found in Gemini response: {clean[:200]}")

        items = json.loads(clean[start:end])
        if not isinstance(items, list):
            raise ValueError("Gemini did not return a JSON array.")

        logger.info(f"[Gemini] Extracted {len(items)} item(s) from receipt.")
        return items, None

    except json.JSONDecodeError as exc:
        logger.error(f"[Gemini] JSON parse error: {exc}")
        return _mock_items(), f"JSON parse error: {exc}"
    except Exception as exc:
        logger.error(f"[Gemini] Call failed: {exc}")
        return _mock_items(), str(exc)


# ---------------------------------------------------------------------------
# Manual entry
# ---------------------------------------------------------------------------

@router.post("/add-item")
async def add_manual_item(body: ManualItemRequest):
    if not body.name.strip():
        raise HTTPException(status_code=400, detail="Item name is required.")

    service = InventoryService()
    today   = datetime.utcnow().date()

    try:
        new_item = await service.add_item(InventoryItemCreate(
            name=body.name.strip()[:255],
            category=body.category,
            quantity=body.quantity,
            unit=body.unit,
            purchase_date=today,
            expiry_date=today + timedelta(days=body.shelf_life_days),
            shelf_life_days=body.shelf_life_days,
            price=body.price,
            source="Virtual Kitchen · Manual Entry",
        ))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to add item: {exc}")

    qty_str = f"{body.quantity} {body.unit}"
    await notify_user(
        body.web_user_id,
        f"✅ <b>Item added to your virtual shelf!</b>\n\n"
        f"📦 <b>{body.name}</b>\n"
        f"   Quantity : {qty_str}\n"
        f"   Category : {body.category}\n"
        f"   Expires in: {body.shelf_life_days} days\n\n"
        f"<i>View your full pantry on the AetherShelf dashboard.</i>",
    )

    return {
        "success": True,
        "item": new_item,
        "message": f"Successfully added {qty_str} {body.name} to your virtual shelf.",
    }


# ---------------------------------------------------------------------------
# Virtual kitchen status
# ---------------------------------------------------------------------------

@router.get("/virtual-status")
async def virtual_kitchen_status(web_user_id: str):
    service  = InventoryService()
    items    = await service.get_all_items()
    expiring = await service.get_expiring_items(3)
    return {
        "success": True,
        "total_items": len(items),
        "expiring_soon": len(expiring),
        "telegram_linked": await is_linked(web_user_id),
        "telegram_id": await get_telegram_id(web_user_id),
        "setup_complete": len(items) > 0,
    }


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _shelf_life(category: str) -> int:
    return {
        "Dairy": 7, "Produce": 5, "Protein": 4, "Bakery": 5,
        "Snacks": 30, "Beverages": 90, "Grains": 180,
        "Condiments": 180, "Frozen": 60,
    }.get(category, 14)


def _safe_float(val) -> Optional[float]:
    try:
        return float(val) if val is not None else None
    except (TypeError, ValueError):
        return None


def _mock_items() -> List[dict]:
    return [
        {"name": "Amul Milk 1L", "quantity": 2, "unit": "L", "price_inr": 62.0, "category": "Dairy"},
        {"name": "Brown Bread", "quantity": 1, "unit": "loaf", "price_inr": 45.0, "category": "Bakery"},
        {"name": "Eggs (12 pack)", "quantity": 12, "unit": "pcs", "price_inr": 96.0, "category": "Protein"},
        {"name": "Basmati Rice 1kg", "quantity": 1, "unit": "kg", "price_inr": 120.0, "category": "Grains"},
        {"name": "Tomatoes", "quantity": 500, "unit": "g", "price_inr": 30.0, "category": "Produce"},
    ]
