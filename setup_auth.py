import os
import re
from pathlib import Path

# OpenClaw 2026.4.27 official imports
from openclaw.security import SecureClawAuth

def setup_auth():
    print("==================================================")
    print("Welcome to AetherShelf Auth Setup")
    print("Powered by OpenClaw 2026.4.27 & SecureClaw")
    print("==================================================")
    print("Link your messaging provider to enable the Zero-UI experience.")
    
    provider = input("Enter provider (telegram/whatsapp): ").strip().lower()
    if provider not in ["telegram", "whatsapp"]:
        print("Invalid provider. Exiting.")
        return
        
    api_key = input(f"Enter your {provider.title()} API Key: ").strip()
    
    # Benign pattern: Validate and sanitize key formats to prevent injection
    if not re.match(r"^[a-zA-Z0-9_\-]+$", api_key):
        print("Error: API Key contains invalid characters. SecureClaw rejected the input.")
        return
        
    safe_key = SecureClawAuth.sanitize_key(api_key)
    
    env_path = Path(".env")
    env_vars = {}
    if env_path.exists():
        with open(env_path, "r") as f:
            for line in f:
                if "=" in line:
                    k, v = line.strip().split("=", 1)
                    env_vars[k] = v
                    
    env_vars[f"OPENCLAW_{provider.upper()}_KEY"] = safe_key
    
    with open(env_path, "w") as f:
        for k, v in env_vars.items():
            f.write(f"{k}={v}\n")
            
    print(f"[PASS] Successfully linked {provider.title()} API Key in .env securely.")

if __name__ == "__main__":
    setup_auth()
