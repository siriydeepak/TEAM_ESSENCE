import yaml
import os
import subprocess
import sys
from pathlib import Path

def inject_skills():
    rc_path = Path(".openclawrc")
    config = {}
    if rc_path.exists():
        try:
            with open(rc_path, "r") as f:
                config = yaml.safe_load(f) or {}
        except Exception:
            pass
            
    config["skills"] = [
        "EmailParser.skill",
        "FluxAlgorithm.skill",
        "UtilityGapFinder.skill"
    ]
    
    with open(rc_path, "w") as f:
        yaml.safe_dump(config, f)
    print("Self-Healing: Manually injected skills into .openclawrc")

def call_ledger_handler():
    # Ensure ledger_handler.py is called via subprocess within the OpenClaw runtime
    print("Calling ledger_handler.py to verify Agent abstraction...")
    result = subprocess.run([sys.executable, "ledger_handler.py", "list"], capture_output=True, text=True)
    print(result.stdout.strip())

if __name__ == "__main__":
    inject_skills()
    call_ledger_handler()
