"""
Analytics and reporting API routes.

This module contains API endpoints for analytics, reporting,
and data insights related to inventory management.
"""

from fastapi import APIRouter
from typing import List, Dict, Any

router = APIRouter()

# In-memory store for expiry logs (will be replaced with database service)
expiry_logs_db = [
    {"id":"e1","item":"Baby Spinach","action":"expired_discarded","date":"2025-05-05","waste_value":35,"category":"Vegetables"},
    {"id":"e2","item":"Chicken Breast","action":"expired_discarded","date":"2025-05-05","waste_value":220,"category":"Protein"},
    {"id":"e3","item":"Amul Greek Yogurt","action":"consumed","date":"2025-05-04","waste_value":0,"category":"Dairy"},
    {"id":"e4","item":"Amul Milk 1L","action":"consumed_before_expiry","date":"2025-05-03","waste_value":0,"category":"Dairy"},
]

@router.get("/summary")
async def get_analytics():
    """Get analytics summary including freshness score and waste metrics."""
    # Import inventory data (this will be replaced with service call)
    from .inventory import inventory_db
    from .smart_cart import smart_cart_db
    
    expiring_soon = len([i for i in inventory_db if i.get("days_left") is not None and 0 <= i["days_left"] <= 3])
    expired = len([i for i in inventory_db if i.get("days_left") is not None and i["days_left"] < 0])
    healthy = len([i for i in inventory_db if i.get("days_left") is not None and i["days_left"] > 7])
    total_waste_inr = sum(i["waste_value"] for i in expiry_logs_db)
    score = max(0, min(100, 100 - expired*20 - expiring_soon*8))
    
    return {
        "total_items": len(inventory_db),
        "expiring_soon": expiring_soon,
        "expired": expired, 
        "healthy": healthy,
        "freshness_score": score,
        "total_waste_inr": round(total_waste_inr, 2),
        "smart_cart_savings_inr": sum((i["original_price"]-i["best_price"]) for i in smart_cart_db)
    }

@router.get("/expiry-logs")
async def get_expiry_logs():
    """Get expiry logs with total waste value."""
    total_waste = sum(i["waste_value"] for i in expiry_logs_db)
    return {"logs": expiry_logs_db, "total_waste_value_inr": round(total_waste, 2)}