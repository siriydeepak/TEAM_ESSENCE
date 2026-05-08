"""
Ledger Handler - Core inventory management utility.
Handles loading, saving, and manipulating pantry inventory data.
"""
from __future__ import annotations

import datetime
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    import yaml
except ImportError:
    yaml = None


def _normalize_name(name: str) -> str:
    """Normalize item name for comparison."""
    return " ".join(str(name).strip().lower().split())


def _parse_date(value: Optional[str]) -> Optional[datetime.date]:
    """Parse date from string in various formats."""
    if value is None:
        return None

    value = str(value).strip()
    if not value:
        return None

    formats = ["%Y-%m-%d", "%Y/%m/%d", "%m/%d/%Y", "%d-%m-%Y", "%d/%m/%Y"]
    for fmt in formats:
        try:
            return datetime.datetime.strptime(value, fmt).date()
        except ValueError:
            continue

    return None


def _format_expiry(value: Optional[str]) -> Optional[str]:
    """Format expiry date to ISO format."""
    if value is None:
        return None
    parsed = _parse_date(value)
    return parsed.isoformat() if parsed else str(value).strip() or None


def _parse_scalar(value: str) -> Any:
    """Parse scalar value from YAML-like string."""
    value = value.strip()
    if value.lower() in {"null", "none", "~"}:
        return None
    if value.lower() in {"true", "yes", "on"}:
        return True
    if value.lower() in {"false", "no", "off"}:
        return False
    if value.startswith(("'", '"')) and value.endswith(("'", '"')) and len(value) >= 2:
        return value[1:-1].replace("''", "'").replace('\\"', '"')
    if value.isdigit() or (value.startswith(("+", "-")) and value[1:].isdigit()):
        try:
            return int(value)
        except ValueError:
            pass
    try:
        return float(value)
    except ValueError:
        pass
    return value


def _scalar_to_yaml(value: Any) -> str:
    """Convert scalar value to YAML string."""
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)

    text = str(value)
    if text == "" or any(ch in text for ch in ":#[]{}&,>?|*-!%@`\n") or text.strip() != text:
        escaped = text.replace("'", "''")
        return f"'{escaped}'"
    return text


def _simple_yaml_dump(data: List[Dict[str, Any]]) -> str:
    """Simple YAML dumper for inventory data."""
    if not data:
        return "[]\n"

    lines: List[str] = []
    for item in data:
        lines.append("-")
        for key, value in item.items():
            lines.append(f"  {key}: {_scalar_to_yaml(value)}")
    return "\n".join(lines) + "\n"


def _simple_yaml_load(text: str) -> List[Dict[str, Any]]:
    """Simple YAML loader for inventory data."""
    lines = [line.rstrip() for line in text.splitlines() if line.strip() and not line.strip().startswith("#")]
    if not lines:
        return []

    if lines[0].strip().startswith("["):
        return []

    items: List[Dict[str, Any]] = []
    current: Dict[str, Any] = {}

    for raw_line in lines:
        stripped = raw_line.lstrip()
        if stripped.startswith("- ") or stripped == "-":
            if current:
                items.append(current)
                current = {}
            remainder = stripped[1:].strip()
            if remainder:
                key, value = remainder.split(":", 1)
                current[key.strip()] = _parse_scalar(value)
        else:
            if ":" not in stripped:
                continue
            key, value = stripped.split(":", 1)
            current[key.strip()] = _parse_scalar(value)

    if current:
        items.append(current)
    return items


def load_ledger(ledger_path: Optional[Path] = None) -> List[Dict[str, Any]]:
    """Load inventory ledger from file."""
    if ledger_path is None:
        return []
    
    path = Path(ledger_path)
    if not path.exists():
        return []
    
    text = path.read_text(encoding="utf-8")
    if not text.strip():
        return []

    if yaml:
        loaded = yaml.safe_load(text)
        if loaded is None:
            return []
        if not isinstance(loaded, list):
            raise ValueError(f"Ledger file must contain a list of items: {path}")
        return loaded

    return _simple_yaml_load(text)


def save_ledger(items: List[Dict[str, Any]], ledger_path: Optional[Path] = None) -> None:
    """Save inventory ledger to file."""
    if ledger_path is None:
        return
    
    path = Path(ledger_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    if yaml:
        body = yaml.safe_dump(items, sort_keys=False, default_flow_style=False)
    else:
        body = _simple_yaml_dump(items)

    temp_path = path.with_suffix(path.suffix + ".tmp")
    temp_path.write_text(body, encoding="utf-8")
    temp_path.replace(path)


def _find_item(items: List[Dict[str, Any]], name: str) -> Optional[Dict[str, Any]]:
    """Find item in inventory by name."""
    normalized = _normalize_name(name)
    for item in items:
        if _normalize_name(item.get("name", "")) == normalized:
            return item
    return None


def _sort_key(item: Dict[str, Any]) -> Any:
    """Sort key for inventory items."""
    expiry = _parse_date(item.get("estimated_expiry"))
    return (expiry or datetime.date.max, _normalize_name(item.get("name", "")))


def get_inventory(ledger_path: Optional[Path] = None) -> List[Dict[str, Any]]:
    """Get sorted inventory items."""
    items = load_ledger(ledger_path)
    return sorted(items, key=_sort_key)


def get_item(name: str, ledger_path: Optional[Path] = None) -> Optional[Dict[str, Any]]:
    """Get specific item from inventory."""
    items = load_ledger(ledger_path)
    return _find_item(items, name)


def get_item_expiry(name: str, ledger_path: Optional[Path] = None) -> Optional[str]:
    """Get expiry date for specific item."""
    item = get_item(name, ledger_path)
    if not item:
        return None
    return item.get("estimated_expiry")


def _build_warnings(name: str, estimated_expiry: Optional[str], items: List[Dict[str, Any]]) -> List[str]:
    """Build collision warnings for duplicate items."""
    warnings: List[str] = []
    existing = _find_item(items, name)
    if existing:
        expiry_date = existing.get("estimated_expiry") or "unknown date"
        warnings.append(
            f"🚨 COLLISION: You already have {existing['name']} expiring on {expiry_date}. Confirm purchase?"
        )
    return warnings


def update_inventory(
    name: str,
    quantity_delta: int,
    estimated_expiry: Optional[str] = None,
    ledger_path: Optional[Path] = None,
) -> Dict[str, Any]:
    """Update inventory item quantity."""
    if not name or not str(name).strip():
        raise ValueError("Item name must not be empty.")
    
    items = load_ledger(ledger_path)
    existing = _find_item(items, name)
    expiry = _format_expiry(estimated_expiry)

    if existing is None:
        if quantity_delta <= 0:
            raise ValueError(f"Cannot subtract {abs(quantity_delta)} from an item that does not exist.")
        new_item = {
            "name": str(name).strip(),
            "quantity": int(quantity_delta),
        }
        if expiry:
            new_item["estimated_expiry"] = expiry
        items.append(new_item)
        save_ledger(items, ledger_path)
        return {"item": new_item, "warnings": _build_warnings(name, expiry, items)}

    current_quantity = int(existing.get("quantity", 0))
    new_quantity = current_quantity + int(quantity_delta)
    if new_quantity < 0:
        raise ValueError(
            f"Cannot remove more '{existing['name']}' than are in the pantry (have {current_quantity}).")

    if new_quantity == 0:
        items.remove(existing)
        save_ledger(items, ledger_path)
        return {"item": {"name": existing["name"], "quantity": 0}, "warnings": _build_warnings(name, expiry, items)}

    existing["quantity"] = new_quantity
    if expiry:
        existing_expiry = _parse_date(existing.get("estimated_expiry"))
        new_expiry = _parse_date(expiry)
        if existing_expiry and new_expiry:
            existing["estimated_expiry"] = min(existing_expiry, new_expiry).isoformat()
        else:
            existing["estimated_expiry"] = expiry

    save_ledger(items, ledger_path)
    return {"item": existing, "warnings": _build_warnings(name, expiry, items)}


def add_item(name: str, quantity: int = 1, estimated_expiry: Optional[str] = None, ledger_path: Optional[Path] = None) -> Dict[str, Any]:
    """Add item to inventory."""
    if quantity <= 0:
        raise ValueError("Quantity to add must be greater than zero.")
    return update_inventory(name, quantity, estimated_expiry, ledger_path)


def remove_item(name: str, quantity: int = 1, ledger_path: Optional[Path] = None) -> Dict[str, Any]:
    """Remove item from inventory."""
    if quantity <= 0:
        raise ValueError("Quantity to remove must be greater than zero.")
    return update_inventory(name, -quantity, None, ledger_path)