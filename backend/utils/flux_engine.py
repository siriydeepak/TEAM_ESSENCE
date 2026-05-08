"""
Flux Engine - Pantry entropy calculation and expiry monitoring utility.
Handles shelf life calculations, item categorization, and expiry tracking.
"""
from __future__ import annotations

import datetime
import sys
import time
import os
import yaml
from pathlib import Path
from typing import Any, Dict, List, Optional

# Decay days for different categories
DECAY_DAYS: Dict[str, int] = {
    "Milk": 3,
    "Vegetables": 5,
    "Dry Goods": 30,
}

# Category keywords for item classification
CATEGORY_KEYWORDS: Dict[str, List[str]] = {
    "Milk": ["milk"],
    "Vegetables": [
        "vegetable",
        "spinach",
        "lettuce",
        "kale",
        "broccoli",
        "carrot",
        "tomato",
        "pepper",
        "cucumber",
        "zucchini",
        "onion",
    ],
    "Dry Goods": [
        "flour",
        "rice",
        "pasta",
        "beans",
        "lentil",
        "cereal",
        "oats",
        "sugar",
        "salt",
        "coffee",
        "tea",
        "bread",
        "cracker",
        "dry",
    ],
}


def parse_expiry(value: Optional[str]) -> Optional[datetime.date]:
    """Parse expiry date from various string formats."""
    if not value:
        return None

    text = str(value).strip()
    if not text:
        return None

    try:
        return datetime.date.fromisoformat(text)
    except ValueError:
        pass

    for fmt in ["%Y-%m-%d", "%Y/%m/%d", "%m/%d/%Y", "%d-%m-%Y", "%d/%m/%Y"]:
        try:
            return datetime.datetime.strptime(text, fmt).date()
        except ValueError:
            continue

    return None


def categorize_item(name: str) -> str:
    """Categorize an item based on its name."""
    normalized = str(name).lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(keyword in normalized for keyword in keywords):
            return category
    return "Dry Goods"


def get_decay_days(item_name: str) -> int:
    """Get the default decay days for an item based on its category."""
    category = categorize_item(item_name)
    return DECAY_DAYS.get(category, DECAY_DAYS["Dry Goods"])


def calculate_days_remaining(expiry_date: datetime.date, reference_date: Optional[datetime.date] = None) -> int:
    """Calculate days remaining until expiry."""
    if reference_date is None:
        reference_date = datetime.date.today()
    return (expiry_date - reference_date).days


def calculate_pantry_entropy(items: List[Dict[str, Any]]) -> float:
    """Calculate pantry entropy based on average days remaining."""
    if not items:
        return 0.0
    
    total_days = 0
    item_count = len(items)
    
    for item in items:
        expiry_date = parse_expiry(item.get("estimated_expiry"))
        if expiry_date is None:
            decay_days = get_decay_days(item.get("name", ""))
            expiry_date = datetime.date.today() + datetime.timedelta(days=decay_days)
        
        days_remaining = calculate_days_remaining(expiry_date)
        total_days += days_remaining
    
    return total_days / item_count if item_count else 0.0


def find_expiring_items(items: List[Dict[str, Any]], threshold_days: int = 2) -> List[Dict[str, Any]]:
    """Find items that are expiring within the threshold."""
    expiring_items = []
    
    for item in items:
        expiry_date = parse_expiry(item.get("estimated_expiry"))
        if expiry_date is None:
            decay_days = get_decay_days(item.get("name", ""))
            expiry_date = datetime.date.today() + datetime.timedelta(days=decay_days)
        
        days_remaining = calculate_days_remaining(expiry_date)
        quantity = int(item.get("quantity", 0))
        
        if 0 <= days_remaining <= threshold_days and quantity > 0:
            expiring_items.append({
                "name": item.get("name", "Unknown Item"),
                "quantity": quantity,
                "estimated_expiry": item.get("estimated_expiry"),
                "days_remaining": days_remaining,
            })
    
    return expiring_items