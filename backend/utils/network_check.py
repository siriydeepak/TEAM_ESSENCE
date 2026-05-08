"""
Network Check - Network connectivity and status utilities.
Handles local IP detection and service availability checks.
"""
import socket
import urllib.request
import urllib.error
from typing import Optional


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


def check_port(host: str, port: int, timeout: float = 0.5) -> bool:
    """Checks if a given port is open/active on the specified host."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            result = s.connect_ex((host, port))
            return result == 0
    except Exception:
        return False


def check_internet_connectivity(host: str = "8.8.8.8", port: int = 53, timeout: float = 3.0) -> bool:
    """Check if internet connectivity is available."""
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error:
        return False


def get_network_status() -> dict:
    """Get comprehensive network status information."""
    return {
        "local_ip": get_local_ip(),
        "ngrok_active": check_ngrok_status(),
        "internet_available": check_internet_connectivity(),
        "local_services": {
            "dashboard": check_port("127.0.0.1", 8501) or check_port("127.0.0.1", 8000),
            "api": check_port("127.0.0.1", 8000),
            "frontend": check_port("127.0.0.1", 3000) or check_port("127.0.0.1", 5173),
        }
    }