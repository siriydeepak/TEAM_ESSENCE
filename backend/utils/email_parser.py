"""
Email Parser - Receipt parsing and item extraction utility.
Handles parsing of receipt text and extracting inventory items.
"""
from __future__ import annotations

import json
from typing import Any, Dict, List, Optional

try:
    import google.generativeai as genai
except ImportError:
    genai = None

SYSTEM_PROMPT = (
    "You are a pantry receipt parser. Extract [Item, Quantity, ExpiryDate] from the provided text "
    "and return it strictly as a JSON object. If the receipt text does not contain an expiry date, estimate one: "
    "3 days for Milk, 5 days for Vegetables, and 30 days for Dry Goods. "
    "Return only valid JSON with keys item, quantity, expiry. If expiry is unavailable, use null."
)


def fetch_mock_emails() -> List[str]:
    """Fetch mock email receipts for testing."""
    return [
        "1L Milk from Blinkit",
        "500g Spinach from Zepto",
        "2 Dry Bread from GroceryHub",
    ]


def call_gemini_parse_api(receipt_text: str, api_key: Optional[str] = None) -> Dict[str, Optional[str]]:
    """Parse a receipt string using Gemini 1.5 Flash via Google Generative AI."""
    if not genai or not api_key:
        # Fallback parsing without AI
        return {
            "item": receipt_text,
            "quantity": "1",
            "expiry": None,
        }
    
    try:
        genai.configure(api_key=api_key)
        
        response = genai.responses.create(
            model="gemini-1.5-flash",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": receipt_text},
            ],
            temperature=0.0,
        )

        content = getattr(response, "output_text", None)
        if content is None:
            output = getattr(response, "output", None)
            if output and isinstance(output, list) and output[0].get("content"):
                content = output[0]["content"][0].get("text")

        if content is None:
            raise ValueError("Gemini response did not contain text.")

        content = content.strip()
        parsed = json.loads(content)
    except Exception as exc:
        print(f"Warning: Gemini parsing failed ({exc}). Falling back to receipt text.")
        return {
            "item": receipt_text,
            "quantity": "1",
            "expiry": None,
        }

    item = parsed.get("item") or receipt_text
    quantity = parsed.get("quantity")
    expiry = parsed.get("expiry")

    return {
        "item": str(item).strip(),
        "quantity": str(quantity) if quantity is not None else "1",
        "expiry": str(expiry).strip() if expiry is not None else None,
    }


def parse_receipts(receipts: List[str], api_key: Optional[str] = None) -> List[Dict[str, Optional[str]]]:
    """Parse multiple receipt texts."""
    parsed: List[Dict[str, Optional[str]]] = []
    for receipt in receipts:
        record = call_gemini_parse_api(receipt, api_key)
        parsed.append(record)
    return parsed


def extract_items_from_receipt(receipt_text: str, api_key: Optional[str] = None) -> List[Dict[str, Any]]:
    """Extract inventory items from receipt text."""
    parsed = call_gemini_parse_api(receipt_text, api_key)
    
    name = parsed.get("item") or "Unknown Item"
    quantity_text = parsed.get("quantity") or "1"
    expiry = parsed.get("expiry")
    
    try:
        quantity = int(quantity_text)
    except ValueError:
        quantity = 1
    
    return [{
        "name": name,
        "quantity": quantity,
        "estimated_expiry": expiry,
        "source": "receipt_parser"
    }]