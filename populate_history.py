import yaml
import random
from datetime import datetime, timedelta
from pathlib import Path

# Absolute paths
ROOT_DIR = Path(__file__).resolve().parent
HISTORY_DIR = ROOT_DIR / "data"

def generate_history():
    HISTORY_DIR.mkdir(parents=True, exist_ok=True)
    history_file = HISTORY_DIR / "consumption_history.yaml"
    
    print("Generating 30 days of historical consumption flux...")
    
    items = ["Milk", "Spinach", "Apples", "Dry Bread", "Coffee Beans"]
    history_data = []
    
    start_date = datetime.now() - timedelta(days=30)
    
    for day_offset in range(30):
        current_date = start_date + timedelta(days=day_offset)
        daily_entries = []
        for item in items:
            # Random consumption mimicking real life flux for impressive UI graphs
            consumed = random.randint(0, 2)
            if consumed > 0:
                daily_entries.append({
                    "item": item,
                    "consumed_qty": consumed,
                    "remaining_qty": random.randint(1, 5)
                })
        
        if daily_entries:
            history_data.append({
                "date": current_date.strftime("%Y-%m-%d"),
                "events": daily_entries
            })
            
    with open(history_file, "w") as f:
        yaml.dump(history_data, f, sort_keys=False)
        
    print(f"[PASS] Generated pitch-ready visual data at {history_file}")

if __name__ == "__main__":
    generate_history()
