"""
Smart cart API routes.

This module contains API endpoints for smart cart functionality,
including price optimization and purchase recommendations.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any

router = APIRouter()

# Pydantic Models
class CartApproval(BaseModel):
    item_id: str
    approved: bool

# In-memory store for smart cart (will be replaced with database service)
smart_cart_db = [
    {"id":"c1","name":"Oat Milk (Barista Blend)","reason":"Out of stock — used daily","urgency":"high","best_price":189,"original_price":240,"source":"Blinkit","savings_pct":21,"approved":False},
    {"id":"c2","name":"Organic Pasture Eggs","reason":"Low stock — 2 remaining","urgency":"medium","best_price":115,"original_price":150,"source":"BigBasket","savings_pct":23,"approved":False},
    {"id":"c3","name":"Britannia Bread WW","reason":"Expires tomorrow","urgency":"high","best_price":42,"original_price":55,"source":"Zepto","savings_pct":24,"approved":True},
]

@router.get("/")
async def get_smart_cart():
    """Get smart cart items with savings calculation."""
    total_savings = sum((i["original_price"] - i["best_price"]) for i in smart_cart_db)
    return {
        "items": smart_cart_db, 
        "total_savings": round(total_savings, 2),
        "pending_count": len([i for i in smart_cart_db if not i["approved"]])
    }

@router.post("/approve")
async def approve_cart_item(approval: CartApproval):
    """Approve or reject a smart cart item."""
    for item in smart_cart_db:
        if item["id"] == approval.item_id:
            item["approved"] = approval.approved
            return {"message": "Updated", "item": item}
    raise HTTPException(status_code=404, detail="Item not found")