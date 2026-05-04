import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from openclaw.events import notify_user
import ledger_handler
from flux_engine import parse_expiry, calculate_days_remaining

def check_collision(item_name: str):
    ledger_path = ROOT_DIR / "pantry_ledger.yaml"
    items = ledger_handler.load_ledger(ledger_path)
    existing = ledger_handler._find_item(items, item_name)
    
    if existing:
        qty = int(existing.get("quantity", 0))
        expiry = parse_expiry(existing.get("estimated_expiry"))
        
        if qty > 0 and expiry:
            days = calculate_days_remaining(expiry)
            if 0 <= days <= 3:
                msg = f"Collision detected! You already have {existing['name']} that expires in {days} days. Do you really need to buy more?"
                notify_user(msg, priority="high")
                return msg
    return "No collision detected."

if __name__ == "__main__":
    item = sys.argv[1] if len(sys.argv) > 1 else "Milk"
    print(check_collision(item))
