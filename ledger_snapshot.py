import sys
import shutil
from datetime import datetime
from pathlib import Path

# Use absolute paths to avoid FileNotFound errors
ROOT_DIR = Path(__file__).resolve().parent
BACKUP_DIR = ROOT_DIR / "backups"

def snapshot_ledger(ledger_path: Path = None):
    if ledger_path is None:
        ledger_path = ROOT_DIR / "pantry_ledger.yaml"
        
    if not ledger_path.exists():
        print(f"Cannot snapshot: {ledger_path} does not exist.")
        return None
        
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = BACKUP_DIR / f"pantry_ledger_{timestamp}.yaml"
    
    shutil.copy2(ledger_path, backup_file)
    print(f"[Snapshot] Ledger securely backed up to {backup_file}")
    return backup_file

if __name__ == "__main__":
    snapshot_ledger()
