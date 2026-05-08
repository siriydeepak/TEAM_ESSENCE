"""
Receipt parsing and ingestion API routes.

This module contains API endpoints for receipt parsing,
item extraction, and collision detection.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import re

router = APIRouter()

# Pydantic Models
class ReceiptInput(BaseModel):
    content: str
    source: str = "gmail"

@router.post("/ingest")
async def ingest_receipt(receipt: ReceiptInput):
    """
    Parse receipt content and extract items with collision detection.
    Detects platform (Blinkit / Zepto / Amazon / BigBasket / Swiggy),
    extracts items, runs collision detection against active inventory.
    """
    # Import inventory data (this will be replaced with service call)
    from .inventory import inventory_db
    
    text = receipt.content
    platform = (
        "Blinkit" if "blinkit" in text.lower() else
        "Zepto" if "zepto" in text.lower() else
        "Amazon Fresh" if "amazon" in text.lower() else
        "BigBasket" if "bigbasket" in text.lower() else
        "Swiggy Instamart" if "swiggy" in text.lower() else
        "Unknown"
    )

    # Extract items from receipt text
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

    # Collision detection
    collisions = []
    for new_item in extracted:
        keyword = new_item["name"].lower().split()[0]
        existing = next((i for i in inventory_db if keyword in i["name"].lower() and i.get("days_left", 99) >= 0), None)
        if existing and existing.get("days_left", 99) <= 5:
            collisions.append(f"Collision! You have {existing['name']} expiring in {existing['days_left']}d — do you need more?")

    return {
        "status": "ingested", 
        "platform": platform, 
        "source": receipt.source,
        "extracted_items": extracted, 
        "collision_alerts": collisions,
        "message": f"Extracted {len(extracted)} items from {platform}"
    }