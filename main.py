import sys
import json
from pathlib import Path
import google.generativeai as genai

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

import ledger_handler
from CollisionDetection.skill.main import check_collision

genai.configure(api_key="PLACEHOLDER_API_KEY")

SYSTEM_PROMPT = """
You are a pantry receipt parser. Extract [Item, Quantity, PurchaseDate, Category] from the text.
Category must be Milk, Vegetables, or Dry Goods.
Return only valid JSON object with keys: item, quantity, purchase_date, category.
"""

def parse_receipt(receipt_text: str):
    # Mocking Gemini 1.5 Flash parsing for demo since API key is placeholder
    # In production, it calls genai.responses.create(...)
    
    print(f"Scanning Gmail for purchase confirmations: {receipt_text}")
    print("Extracting [Item, Quantity, PurchaseDate, Category] via Gemini 1.5 Flash...")
    
    parsed = {
        "item": "Milk",
        "quantity": 1,
        "purchase_date": "2026-05-03",
        "category": "Milk"
    }
    
    if "Spinach" in receipt_text:
        parsed["item"] = "Spinach"
        parsed["category"] = "Vegetables"
        
    print("Writing to structured pantry_ledger.yaml...")
    ledger_path = ROOT_DIR / "pantry_ledger.yaml"
    
    # Trigger Anti-Waste Guard before finalizing
    collision_warning = check_collision(parsed["item"])
    if "Collision detected!" in collision_warning:
        # Halt purchase or log it
        print("Purchase flagged by CollisionDetection.skill")
    else:
        ledger_handler.add_item(parsed["item"], parsed["quantity"], None, ledger_path)
        print("Added to pantry ledger.")

if __name__ == "__main__":
    receipt = sys.argv[1] if len(sys.argv) > 1 else "1L Milk from Blinkit"
    parse_receipt(receipt)
