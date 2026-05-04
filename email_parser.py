from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

import google.generativeai as genai

CURRENT_DIR = Path(__file__).resolve().parent
PARENT_DIR = CURRENT_DIR.parent
sys.path.insert(0, str(PARENT_DIR))

from ledger_handler import add_item


genai.configure(api_key="PLACEHOLDER_API_KEY")

SYSTEM_PROMPT = (
    "You are a pantry receipt parser. Extract [Item, Quantity, ExpiryDate] from the provided text "
    "and return it strictly as a JSON object. If the receipt text does not contain an expiry date, estimate one: "
    "3 days for Milk, 5 days for Vegetables, and 30 days for Dry Goods. "
    "Return only valid JSON with keys item, quantity, expiry. If expiry is unavailable, use null."
)


def fetch_mock_emails() -> List[str]:
    return [
        "1L Milk from Blinkit",
        "500g Spinach from Zepto",
        "2 Dry Bread from GroceryHub",
    ]


def call_gemini_parse_api(receipt_text: str) -> Dict[str, Optional[str]]:
    """Parse a receipt string using Gemini 1.5 Flash via Google Generative AI."""
    try:
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


def parse_receipts(receipts: List[str]) -> List[Dict[str, Optional[str]]]:
    parsed: List[Dict[str, Optional[str]]] = []
    for receipt in receipts:
        record = call_gemini_parse_api(receipt)
        parsed.append(record)
    return parsed


def main() -> None:
    ledger_path = PARENT_DIR / "pantry_ledger.yaml"
    receipts = fetch_mock_emails()
    parsed_items = parse_receipts(receipts)

    for parsed in parsed_items:
        name = parsed.get("item") or "Unknown Item"
        quantity_text = parsed.get("quantity") or "1"
        expiry = parsed.get("expiry")

        try:
            quantity = int(quantity_text)
        except ValueError:
            quantity = 1

        result = add_item(name, quantity, expiry, ledger_path)
        warnings = result.get("warnings", [])
        for warning in warnings:
            print(warning)


if __name__ == "__main__":
    main()
