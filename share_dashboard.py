import os
import subprocess
from dotenv import load_dotenv

load_dotenv()
PORT = os.getenv("DASHBOARD_PORT", "8000")

def share_via_localtunnel():
    print("==================================================")
    print("AetherShelf Universal Dashboard - Remote Tunnel")
    print("==================================================")
    print(f"Starting Localtunnel on local port {PORT}...")
    print("To stop, press Ctrl+C")
    
    try:
        # Localtunnel generates a public URL securely (no signup needed unlike Ngrok sometimes)
        subprocess.run(
            ["npx", "localtunnel", "--port", str(PORT), "--subdomain", "aethershelf-demo-live"],
            shell=True,
            check=True
        )
    except KeyboardInterrupt:
        print("\nTunnel closed securely.")
    except Exception as e:
        print(f"Error starting tunnel: {e}")
        print("Tip: Ensure Node.js and npx are installed (e.g., 'npm install -g localtunnel').")

if __name__ == "__main__":
    share_via_localtunnel()
