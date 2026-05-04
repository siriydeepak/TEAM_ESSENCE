from __future__ import annotations

import sys
import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import google.generativeai as genai

CURRENT_DIR = Path(__file__).resolve().parent
ROOT_DIR = CURRENT_DIR.parent
sys.path.insert(0, str(ROOT_DIR))

from ledger_handler import load_ledger


genai.configure(api_key="PLACEHOLDER_API_KEY")

SYSTEM_PROMPT = (
    "You are a pantry assistant. Given the expiring items, answer the following as a single WhatsApp-style"
    " Proactive Suggestion. Use an ingredient costing less than $2 to create a high-value meal that uses the expiring items. "
    "Format the response exactly like: 'Your Spinach is expiring! Buy $1 of cream to make Creamed Spinach—this unlocks 80% of your expiring inventory'."
)


def parse_expiry(value: Any) -> Optional[datetime.date]:
    if value is None:
        return None

    text = str(value).strip()
    if not text:
        return None

    try:
        return datetime.date.fromisoformat(text)
    except ValueError:
        pass

    formats = ["%Y-%m-%d", "%Y/%m/%d", "%m/%d/%Y", "%d-%m-%Y", "%d/%m/%Y"]
    for fmt in formats:
        try:
            return datetime.datetime.strptime(text, fmt).date()
        except ValueError:
            continue

    return None


def find_expiring_items(ledger_path: Path) -> List[Dict[str, Any]]:
    items = load_ledger(ledger_path)
    today = datetime.date.today()
    expiring: List[Dict[str, Any]] = []

    for item in items:
        expiry = parse_expiry(item.get("estimated_expiry"))
        if expiry is None:
            continue

        remaining = (expiry - today).days
        if 0 <= remaining < 2:
            expiring.append({
                "name": item.get("name", "Unknown Item"),
                "quantity": item.get("quantity", 0),
                "estimated_expiry": item.get("estimated_expiry"),
                "days_remaining": remaining,
            })

    return expiring


def build_gemini_prompt(expiring_items: List[Dict[str, Any]]) -> str:
    lines = ["The following items are expiring soon:"]
    for item in expiring_items:
        lines.append(
            f"- {item['name']} x{item['quantity']} (expiry: {item['estimated_expiry']}, days remaining: {item['days_remaining']})"
        )

    lines.append("")
    lines.append(
        "What is one missing ingredient I can buy for less than $2 to create a high-value meal using these expiring items?"
    )
    return "\n".join(lines)


def call_gemini_suggestion(expiring_items: List[Dict[str, Any]]) -> str:
    prompt = build_gemini_prompt(expiring_items)
    try:
        response = genai.responses.create(
            model="gemini-1.5-flash",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
        )

        content = getattr(response, "output_text", None)
        if content is None:
            output = getattr(response, "output", None)
            if output and isinstance(output, list) and output[0].get("content"):
                content = output[0]["content"][0].get("text")

        if not content:
            raise ValueError("Gemini response did not contain text.")

        return content.strip()
    except Exception as exc:
        return f"Proactive Suggestion: Unable to generate suggestion ({exc})"


def main() -> None:
    ledger_path = ROOT_DIR / "pantry_ledger.yaml"
    expiring_items = find_expiring_items(ledger_path)

    if not expiring_items:
        print("No items are expiring in less than 48 hours.")
        return

    suggestion = call_gemini_suggestion(expiring_items)
    if not suggestion.startswith("Proactive Suggestion:"):
        suggestion = f"Proactive Suggestion: {suggestion}"

    print(suggestion)


if __name__ == "__main__":
    main()
