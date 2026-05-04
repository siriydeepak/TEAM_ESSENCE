import sys
import datetime
import shutil
from pathlib import Path

# OpenClaw 2026.4.27 official imports
from openclaw.skills import OpenClawSkill, tool
from openclaw.events import notify_user
from openclaw.security import sanitize_ocr_input

# Path logic to import root scripts securely using absolute paths
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

import ledger_handler
from flux_engine import calculate_days_remaining, get_decay_days, parse_expiry, TODAY
from ledger_snapshot import snapshot_ledger

class PantryIntelSkill(OpenClawSkill):
    """
    Core logic for AetherShelf bot.
    Integrates ledger_handler, flux_engine, and robust snapshot capabilities.
    """
    def __init__(self):
        super().__init__()
        self.ledger_path = ROOT_DIR / "pantry_ledger.yaml"

    @tool(name="update_inventory")
    def update_inventory(self, item_name: str, quantity: int, expiry_date: str = None):
        """Updates the pantry inventory securely."""
        safe_name = sanitize_ocr_input(item_name)
        result = ledger_handler.add_item(safe_name, quantity, expiry_date, self.ledger_path)
        return result

    @tool(name="predict_depletion")
    def predict_depletion(self):
        """
        Autonomous Flux: Triggered by file_watcher on ledger changes.
        """
        # Data Integrity: Take a snapshot prior to processing
        snapshot_ledger(self.ledger_path)
        
        items = ledger_handler.load_ledger(self.ledger_path)
        alerts = []
        for item in items:
            name = item.get("name", "Unknown")
            quantity = int(item.get("quantity", 0))
            if quantity <= 0:
                continue
                
            expiry = parse_expiry(item.get("estimated_expiry"))
            if not expiry:
                decay = get_decay_days(name)
                expiry = TODAY + datetime.timedelta(days=decay)
                
            days_remaining = calculate_days_remaining(expiry)
            
            # Predict item will run out in < 3 days (Utility Gap check)
            if days_remaining < 3:
                alert_msg = f"⚠️ AetherShelf Alert: Based on your consumption flux, you will run out of {name} by {expiry.isoformat()}. Should I add this to your list?"
                # OpenClaw message hook for Zero-UI push notifications
                notify_user(message=alert_msg, priority="high")
                alerts.append(alert_msg)
                
        return alerts

    @tool(name="generate_shopping_list")
    def generate_shopping_list(self):
        """Compiles a list of zero-stock items."""
        items = ledger_handler.load_ledger(self.ledger_path)
        shopping_list = []
        for item in items:
            quantity = int(item.get("quantity", 0))
            if quantity == 0:
                shopping_list.append(item.get("name"))
        return shopping_list

    @tool(name="revert_ledger")
    def revert_ledger(self, backup_filename: str = None):
        """
        Reverts the pantry ledger to the most recent backup, or a specified backup.
        Essential for hackathon demo stability and error recovery.
        """
        backup_dir = ROOT_DIR / "backups"
        if not backup_dir.exists():
            return "No backups directory found."

        if backup_filename:
            target_backup = backup_dir / backup_filename
        else:
            backups = list(backup_dir.glob("pantry_ledger_*.yaml"))
            if not backups:
                return "No backups found."
            # Sort chronologically to get the most recent
            target_backup = sorted(backups)[-1]

        if not target_backup.exists():
            return f"Backup {target_backup.name} not found."

        shutil.copy2(target_backup, self.ledger_path)
        return f"Successfully reverted ledger to {target_backup.name}."
