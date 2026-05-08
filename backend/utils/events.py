"""
Events - Event logging and notification utilities.
Handles system events, notifications, and logging functionality.
"""
import datetime
from pathlib import Path
from typing import Optional, Dict, Any


def notify_user(message: str, priority: str = "normal", log_path: Optional[Path] = None) -> None:
    """Log notification message with timestamp and priority."""
    if log_path is None:
        log_path = Path.cwd() / "logs" / "system.log"
    
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"{ts} [NOTIFY | Priority: {priority.upper()}] {message}"
    
    print(f"\n{line}\n")
    
    try:
        log_path.parent.mkdir(parents=True, exist_ok=True)
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except OSError as e:
        print(f"Warning: Could not write to log file: {e}")


def log_inventory_event(event_type: str, item_name: str, details: Dict[str, Any], log_path: Optional[Path] = None) -> None:
    """Log inventory-related events."""
    if log_path is None:
        log_path = Path.cwd() / "logs" / "inventory.log"
    
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"{ts} [INVENTORY | {event_type.upper()}] {item_name}: {details}"
    
    try:
        log_path.parent.mkdir(parents=True, exist_ok=True)
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except OSError as e:
        print(f"Warning: Could not write to inventory log: {e}")


def log_api_event(method: str, endpoint: str, status_code: int, response_time: float, log_path: Optional[Path] = None) -> None:
    """Log API request events."""
    if log_path is None:
        log_path = Path.cwd() / "logs" / "api.log"
    
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"{ts} [API] {method} {endpoint} - {status_code} ({response_time:.3f}s)"
    
    try:
        log_path.parent.mkdir(parents=True, exist_ok=True)
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except OSError as e:
        print(f"Warning: Could not write to API log: {e}")


def create_system_event(event_type: str, message: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Create a structured system event."""
    return {
        "timestamp": datetime.datetime.now().isoformat(),
        "event_type": event_type,
        "message": message,
        "metadata": metadata or {},
        "id": f"{event_type}_{datetime.datetime.now().timestamp()}"
    }


def format_alert_message(alert_type: str, item_name: str, days_remaining: int) -> str:
    """Format alert message for different alert types."""
    if alert_type == "expiry_warning":
        return f"⚠️ {item_name} expires in {days_remaining} day{'s' if days_remaining != 1 else ''}"
    elif alert_type == "expired":
        return f"🚨 {item_name} has expired"
    elif alert_type == "low_stock":
        return f"📦 {item_name} is running low"
    elif alert_type == "restock_suggestion":
        return f"🛒 Consider restocking {item_name}"
    else:
        return f"ℹ️ {item_name}: {alert_type}"