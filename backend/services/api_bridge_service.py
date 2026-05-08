"""
API Bridge Service - Consolidated API functionality from TEAM_ESSENCE.
Handles dashboard API, cloud sync, push notifications, and system state management.
"""

import os
import json
import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

from ..models.system import (
    SystemState, NetworkStatus, SystemAlert, AlertType,
    CloudSyncData, InventoryUpdateRequest, ApiResponse
)
from ..utils.ledger_handler import load_ledger, add_item
from ..utils.flux_engine import (
    parse_expiry, get_decay_days, calculate_days_remaining,
    calculate_pantry_entropy, find_expiring_items
)
from ..utils.network_check import get_local_ip, check_ngrok_status


class ApiBridgeService:
    """Service for handling API bridge functionality."""
    
    def __init__(self, port: int = 8000):
        self.port = port
        self.cloud_mode = os.getenv("CLOUD_MODE", "false").lower() == "true"
        self.api_key = os.getenv("AETHERSHELF_CLOUD_API_KEY", "secure_claw_live_demo_123")
        self.cloud_ledger_cache: List[Dict[str, Any]] = []
        self.last_heartbeat: Optional[datetime.datetime] = None
        self.push_subscribers: List[Dict[str, Any]] = []
        
    def get_system_state(self, ledger_path: Optional[Path] = None) -> SystemState:
        """Get comprehensive system state."""
        # Load inventory data
        if self.cloud_mode:
            items = self.cloud_ledger_cache
            heartbeat_active = (
                self.last_heartbeat is not None and 
                (datetime.datetime.now() - self.last_heartbeat).seconds < 300
            )
        else:
            items = load_ledger(ledger_path) if ledger_path else []
            heartbeat_active = True  # Local mode assumes direct sync
        
        # Process inventory items
        formatted_ledger = []
        alerts = []
        
        for item in items:
            name = item.get("name", "Unknown")
            qty = int(item.get("quantity", 0))
            expiry_date = parse_expiry(item.get("estimated_expiry"))
            
            if not expiry_date:
                decay = get_decay_days(name)
                expiry_date = datetime.date.today() + datetime.timedelta(days=decay)
            
            days = calculate_days_remaining(expiry_date)
            
            formatted_ledger.append({
                "name": name,
                "quantity": qty,
                "days": days
            })
            
            # Generate alerts for expiring items
            if days < 3 and qty > 0:
                alerts.extend(self._generate_alerts(name, days))
        
        # Calculate entropy score
        active_items = [i for i in formatted_ledger if i["quantity"] > 0]
        entropy_score = (
            round(sum(i["days"] for i in active_items) / len(active_items), 1) 
            if active_items else 0.0
        )
        
        # Load system logs
        logs = self._load_system_logs()
        
        # Create network status
        network = NetworkStatus(
            local_ip=get_local_ip(),
            local_url=f"http://{get_local_ip()}:{self.port}",
            public_active=self.cloud_mode,
            ngrok_active=check_ngrok_status(),
            heartbeat_active=heartbeat_active
        )
        
        return SystemState(
            status="healthy" if heartbeat_active else "partial",
            entropy_score=entropy_score,
            ledger=formatted_ledger,
            logs=logs,
            alerts=alerts,
            network=network
        )
    
    def _generate_alerts(self, item_name: str, days_remaining: int) -> List[SystemAlert]:
        """Generate alerts for expiring items."""
        alerts = []
        
        # Restock alert
        alerts.append(SystemAlert(
            id=f"{item_name}_restock",
            type=AlertType.RESTOCK,
            item=item_name,
            message=f"⚠️ AetherShelf Alert: Based on your consumption flux, you will run out of {item_name} in {days_remaining} days. Should I add this to your list?",
            priority="high" if days_remaining <= 1 else "normal"
        ))
        
        # Specific item-based suggestions
        if "spinach" in item_name.lower():
            alerts.append(SystemAlert(
                id=f"{item_name}_gap",
                type=AlertType.UTILITY_GAP,
                item=item_name,
                message="Buy $1 of cream to make Creamed Spinach—this unlocks 80% of your current expiring inventory.",
                priority="normal"
            ))
        elif "milk" in item_name.lower() or "bread" in item_name.lower():
            alerts.append(SystemAlert(
                id=f"{item_name}_collision",
                type=AlertType.COLLISION,
                item=item_name,
                message=f"Collision detected! You already have {item_name} that expires in {days_remaining} days. Do you really need to buy more?",
                priority="normal"
            ))
        
        return alerts
    
    def _load_system_logs(self, max_lines: int = 50) -> str:
        """Load recent system logs."""
        log_path = Path.cwd() / "logs" / "system.log"
        
        if not log_path.exists():
            return "Awaiting system logs..."
        
        try:
            with open(log_path, "r", encoding="utf-8", errors="replace") as f:
                lines = f.readlines()
                return "".join(lines[-max_lines:])
        except Exception:
            return "Error loading system logs..."
    
    def sync_cloud_ledger(self, data: CloudSyncData, auth_token: str) -> ApiResponse:
        """Sync ledger data from cloud source."""
        if auth_token != f"Bearer {self.api_key}":
            return ApiResponse(
                status="error",
                message="Authentication failed"
            )
        
        self.cloud_ledger_cache = data.ledger
        self.last_heartbeat = datetime.datetime.now()
        
        return ApiResponse(
            status="success",
            message="Cloud ledger synced via webhook"
        )
    
    def update_inventory(self, update: InventoryUpdateRequest, ledger_path: Optional[Path] = None) -> ApiResponse:
        """Update inventory item."""
        try:
            result = add_item(
                update.item_name, 
                update.quantity, 
                None, 
                ledger_path
            )
            return ApiResponse(
                status="success",
                message="Inventory updated successfully",
                data=result
            )
        except Exception as e:
            return ApiResponse(
                status="error",
                message=f"Failed to update inventory: {str(e)}"
            )
    
    def get_public_url(self) -> Dict[str, Optional[str]]:
        """Get public URL if available."""
        url_file = Path.cwd() / "public_url.txt"
        
        if url_file.exists():
            try:
                with open(url_file, "r") as f:
                    url = f.read().strip()
                    return {"url": url}
            except Exception:
                pass
        
        return {"url": None}
    
    def subscribe_push_notifications(self, subscription: Dict[str, Any]) -> Dict[str, Any]:
        """Subscribe to push notifications."""
        # Deduplicate by endpoint
        self.push_subscribers = [
            s for s in self.push_subscribers 
            if s["endpoint"] != subscription["endpoint"]
        ]
        self.push_subscribers.append(subscription)
        
        return {
            "status": "subscribed",
            "total": len(self.push_subscribers)
        }
    
    def send_test_push(self) -> Dict[str, Any]:
        """Send test push notification."""
        return {
            "status": "sent",
            "subscribers": len(self.push_subscribers)
        }
    
    def get_vapid_public_key(self) -> str:
        """Get VAPID public key for push notifications."""
        return os.getenv("VAPID_PUBLIC_KEY", "")
    
    def trigger_demo_mode(self) -> ApiResponse:
        """Trigger demo mode functionality."""
        # This would typically trigger external scripts or processes
        # For now, return a success response
        return ApiResponse(
            status="success",
            message="Demo mode triggered successfully"
        )