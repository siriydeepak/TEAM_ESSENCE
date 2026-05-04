"""
AetherShelf Public Tunnel
Uses pyngrok (auto-downloads ngrok binary, no account needed for basic use).
URL is printed to stdout AND saved to public_url.txt for the dashboard.

Usage:
    python start_public_link.py

The tunnel URL works from ANY network / WiFi — share it with judges/anyone.
"""
import os
import sys
import time
from pathlib import Path
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent
URL_FILE = ROOT_DIR / "public_url.txt"


def start_tunnel(port: int):
    print("=" * 56)
    print("  AetherShelf Sentinel - Public Tunnel (ngrok)")
    print("=" * 56)
    print(f"  Exposing local port {port} to the internet...")
    print()

    try:
        from pyngrok import ngrok, conf

        # Use ngrok authtoken if set in .env (optional but gives longer sessions)
        ngrok_token = os.getenv("NGROK_AUTHTOKEN", "")
        if ngrok_token:
            conf.get_default().auth_token = ngrok_token
            print(f"  [+] Using NGROK_AUTHTOKEN for authenticated session.")
        else:
            print("  [i] No NGROK_AUTHTOKEN in .env - using anonymous session.")
            print("      (Sessions last ~2h. Add NGROK_AUTHTOKEN to .env for unlimited.)")
        print()

        # Open the HTTP tunnel
        tunnel = ngrok.connect(port, "http")
        public_url = tunnel.public_url

        # ngrok always gives http:// - upgrade to https://
        if public_url.startswith("http://"):
            public_url = "https://" + public_url[7:]

        print("=" * 56)
        print("  [OK] PUBLIC URL - share this with ANYONE:")
        print(f"       {public_url}")
        print("=" * 56)
        print()
        print("  The URL works on any WiFi / mobile network.")
        print("  Keep this terminal open to keep the tunnel alive.")
        print()

        # Save for the /api/public-url dashboard endpoint
        URL_FILE.write_text(public_url, encoding="utf-8")

        # Block forever (keep tunnel alive)
        try:
            ngrok.get_ngrok_process().proc.wait()
        except KeyboardInterrupt:
            print("\n[*] Shutting down tunnel...")
            ngrok.kill()
            if URL_FILE.exists():
                URL_FILE.unlink(missing_ok=True)
            print("[*] Tunnel closed cleanly.")

    except ImportError:
        print("[!] pyngrok not installed. Run:  pip install pyngrok")
        sys.exit(1)
    except Exception as exc:
        print(f"[!] Tunnel error: {exc}")
        print()
        print("--- Falling back to localhost.run (SSH) ---")
        _ssh_fallback(port)


def _ssh_fallback(port: int):
    """Fallback: localhost.run via SSH (no binary needed, less stable)."""
    import subprocess
    import re
    import threading

    URL_PAT = re.compile(r"(https://[a-zA-Z0-9\-]+\.lhr\.life)")
    cmd = [
        "ssh", "-o", "StrictHostKeyChecking=no",
        "-o", "ServerAliveInterval=30",
        "-o", "ConnectTimeout=20",
        "-R", f"80:localhost:{port}",
        "nokey@localhost.run"
    ]

    print(f"[*] Connecting via localhost.run (SSH)...")
    while True:
        try:
            proc = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=0
            )
            url_found = False

            def _read(pipe):
                nonlocal url_found
                for raw in iter(pipe.readline, b""):
                    line = re.sub(r"\x1b\[[0-9;?]*[A-Za-z]", "", raw.decode("utf-8", errors="replace"))
                    sys.stdout.write(line); sys.stdout.flush()
                    m = URL_PAT.search(line)
                    if m and not url_found:
                        url = m.group(1)
                        url_found = True
                        print(f"\n[OK] PUBLIC URL: {url}\n")
                        URL_FILE.write_text(url, encoding="utf-8")

            for pipe in (proc.stdout, proc.stderr):
                threading.Thread(target=_read, args=(pipe,), daemon=True).start()
            proc.wait()
        except KeyboardInterrupt:
            if URL_FILE.exists():
                URL_FILE.unlink(missing_ok=True)
            break
        except Exception as e:
            print(f"[!] SSH error: {e}")
        print("[!] Reconnecting in 3s...")
        time.sleep(3)


if __name__ == "__main__":
    load_dotenv()
    port = int(os.getenv("DASHBOARD_PORT", "8000"))
    start_tunnel(port)
