import sys, os
sys.path.insert(0, r"c:\Users\Admin\aethershelf")
os.chdir(r"c:\Users\Admin\aethershelf")

from dotenv import load_dotenv
load_dotenv()

try:
    import fastapi; print("fastapi OK")
    import uvicorn; print("uvicorn OK")
    import yaml; print("pyyaml OK")
    import plotly; print("plotly OK")
    import pywebpush; print("pywebpush OK")
    import cryptography; print("cryptography OK")
    import ledger_handler; print("ledger_handler OK")
    from flux_engine import parse_expiry, get_decay_days, calculate_days_remaining, TODAY
    print("flux_engine OK")
    from pathlib import Path
    items = ledger_handler.load_ledger(Path("pantry_ledger.yaml"))
    print(f"Ledger OK: {len(items)} items loaded")
    for item in items:
        print(f"  {item['name']} | qty={item['quantity']} | expiry={item.get('estimated_expiry', 'auto')}")
    print("\n>>> ALL CHECKS PASSED — run: python main.py <<<")
except Exception as e:
    print(f"FAILED: {e}")
    import traceback; traceback.print_exc()
