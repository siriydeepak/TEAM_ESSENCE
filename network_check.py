import socket
import urllib.request
import urllib.error

def get_local_ip() -> str:
    """Returns the local network IP address of the machine."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Attempt to connect to an external IP to route through the default interface
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

def check_ngrok_status() -> bool:
    """
    Checks if the local ngrok API is reachable to see if the tunnel is active.
    This fulfills the Failsafe Logic requirement for internet dropouts.
    """
    try:
        # ngrok's local API typically runs on 4040
        urllib.request.urlopen("http://127.0.0.1:4040/api/tunnels", timeout=0.5)
        return True
    except (urllib.error.URLError, socket.timeout):
        return False
