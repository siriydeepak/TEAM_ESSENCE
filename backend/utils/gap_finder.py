"""
Gap Finder - Recipe suggestion and inventory optimization utility.
Analyzes expiring items and suggests recipes to maximize inventory usage.
"""
from __future__ import annotations

import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    import google.generativeai as genai
except ImportError:
    genai = None

SYSTEM_PROMPT = (
    "You are a pantry assistant. Given the expiring items, answer the following as a single WhatsApp-style"
    " Proactive Suggestion. Use an ingredient costing less than $2 to create a high-value meal that uses the expiring items. "
    "Format the response exactly like: 'Your Spinach is expiring! Buy $1 of cream to make Creamed Spinach—this unlocks 80% of your expiring inventory'."
)


def parse_expiry(value: Any) -> Optional[datetime.date]:
    """Parse expiry date from various formats."""
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


def find_expiring_items(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Find items that are expiring within 2 days."""
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
    """Build a prompt for Gemini API to generate recipe suggestions."""
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


def call_gemini_suggestion(expiring_items: List[Dict[str, Any]], api_key: Optional[str] = None) -> str:
    """Generate recipe suggestion using Gemini AI."""
    if not genai or not api_key:
        return "Proactive Suggestion: AI service unavailable. Consider using expiring items in a simple recipe."
    
    try:
        genai.configure(api_key=api_key)
        prompt = build_gemini_prompt(expiring_items)
        
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


def generate_recipe_suggestions(items: List[Dict[str, Any]], api_key: Optional[str] = None) -> List[Dict[str, Any]]:
    """Generate recipe suggestions for expiring items."""
    expiring_items = find_expiring_items(items)
    
    if not expiring_items:
        return []
    
    suggestion = call_gemini_suggestion(expiring_items, api_key)
    if not suggestion.startswith("Proactive Suggestion:"):
        suggestion = f"Proactive Suggestion: {suggestion}"
    
    return [{
        "suggestion": suggestion,
        "expiring_items": expiring_items,
        "confidence": 80,  # Default confidence
        "category": "Recipe Suggestion",
        "cuisine": "General"
    }]