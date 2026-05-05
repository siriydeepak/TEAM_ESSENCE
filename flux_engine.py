from __future__ import annotations

import datetime
import sys
import time
import os
import yaml
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT_DIR))

from ledger_handler import load_ledger, save_ledger

DECAY_DAYS: Dict[str, int] = {
    "Milk": 3,
    "Vegetables": 5,
    "Dry Goods": 30,
}

TODAY = datetime.date(2026, 5, 2)

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
    normalized = str(name).lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(keyword in normalized for keyword in keywords):
            return category
    return "Dry Goods"


def get_decay_days(item_name: str) -> int:
    category = categorize_item(item_name)
    return DECAY_DAYS.get(category, DECAY_DAYS["Dry Goods"])


def calculate_days_remaining(expiry_date: datetime.date) -> int:
    return (expiry_date - TODAY).days


def main() -> None:
    ledger_path = ROOT_DIR / "pantry_ledger.yaml"

    print("Flux Engine starting. Monitoring ledger for changes...")
    last_mtime = 0

    while True:
        try:
            current_mtime = os.path.getmtime(ledger_path)
        except OSError:
            current_mtime = last_mtime

        if current_mtime != last_mtime:
            last_mtime = current_mtime
            items = load_ledger(ledger_path)

            expired_count = 0
            total_days = 0
            item_count = len(items)
            
            trigger_action = False
            expiring_items_detected = []

            for item in items:
                expiry_date = parse_expiry(item.get("estimated_expiry"))
                if expiry_date is None:
                    decay_days = get_decay_days(item.get("name", ""))
                    expiry_date = TODAY + datetime.timedelta(days=decay_days)
                    item["estimated_expiry"] = expiry_date.isoformat()

                days_remaining = calculate_days_remaining(expiry_date)
                
                quantity = int(item.get("quantity", 0))

                if days_remaining <= 0 and quantity > 0:
                    name = str(item.get("name", "Unknown Item"))
                    if not name.startswith("[EXPIRED] "):
                        item["name"] = f"[EXPIRED] {name}"
                    item["quantity"] = 0
                    expired_count += 1
                    days_remaining = 0
                
                # Check threshold for proactive trigger
                if 0 <= days_remaining < 2 and quantity > 0:
                    trigger_action = True
                    expiring_items_detected.append(item.get("name"))

                total_days += days_remaining

            pantry_entropy = total_days / item_count if item_count else 0.0
            
            save_ledger(items, ledger_path)
            
            # Re-read mtime since we just saved it to avoid double-triggering
            try:
                last_mtime = os.path.getmtime(ledger_path)
            except OSError:
                pass

            print(
                f"HEARTBEAT: Pantry Entropy is {pantry_entropy:.2f} days. {expired_count} items have expired today."
            )
            
            if trigger_action:
                # Output structured OpenClaw Action
                action = {
                    "openclaw_action": "trigger_skill",
                    "target_skill": "UtilityGapFinder.skill",
                    "reason": f"Stock near depletion: {', '.join(expiring_items_detected)}",
                }
                print(yaml.dump(action, sort_keys=False).strip())
                sys.stdout.flush()

        time.sleep(1)


if __name__ == "__main__":
    main()
