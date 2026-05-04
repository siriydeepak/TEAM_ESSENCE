import sys
import os
import requests
from dotenv import load_dotenv
from pathlib import Path

# Load SecureClaw env
ROOT_DIR = Path(__file__).resolve().parent.parent
env_path = ROOT_DIR / ".env"
load_dotenv(dotenv_path=env_path)

AETHERSHELF_CLOUD_API_KEY = os.getenv("AETHERSHELF_CLOUD_API_KEY", "secure_claw_live_demo_123")
CLOUD_URL = os.getenv("AETHERSHELF_CLOUD_URL", "http://localhost:8080/api/update")

def sync_to_cloud(ledger_items: list):
    """
    Secure Webhook logic:
    Pushes the entire pantry ledger to the Cloud Run Dashboard.
    Triggered every time the local agent updates the ledger.
    """
    headers = {
        "Authorization": f"Bearer {AETHERSHELF_CLOUD_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "ledger": ledger_items
    }
    
    try:
        response = requests.post(CLOUD_URL, json=payload, headers=headers, timeout=5)
        if response.status_code == 200:
            print("🟢 Secure Webhook: Successfully synced local ledger to Cloud Dashboard.")
        else:
            print(f"🔴 Secure Webhook Failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"⚠️ Cloud Sync unreachable (Network might be down): {e}")

# If we want to test it standalone:
if __name__ == "__main__":
    import yaml
    ledger_path = ROOT_DIR / "pantry_ledger.yaml"
    if ledger_path.exists():
        with open(ledger_path, "r") as f:
            data = yaml.safe_load(f) or []
            sync_to_cloud(data)
