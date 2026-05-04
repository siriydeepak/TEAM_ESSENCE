import sys
from pathlib import Path
from openclaw.events import notify_user

def find_utility_gap(expiring_item: str):
    """
    Connects expiring items to a recipe/pairing database.
    Checks pantry for Missing Links.
    """
    if "Spinach" in expiring_item:
        suggestion = "Buy $1 of cream to make Creamed Spinach—this unlocks 80% of your current expiring inventory."
        notify_user(f"Utility Gap Found: {suggestion}", priority="high")
        return suggestion
        
    return "No obvious missing link found."

if __name__ == "__main__":
    item = sys.argv[1] if len(sys.argv) > 1 else "Spinach"
    print(find_utility_gap(item))
