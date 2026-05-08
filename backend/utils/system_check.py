"""
System Check - System diagnostics and health monitoring utilities.
Handles environment validation and service status checks.
"""
import os
import socket
from pathlib import Path
from typing import Dict, Any, Optional


def check_port(host: str, port: int, timeout: float = 0.5) -> bool:
    """Checks if a given local port is open/active."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            result = s.connect_ex((host, port))
            return result == 0
    except Exception:
        return False


def check_env_file(env_path: Optional[Path] = None) -> bool:
    """Verifies that environment file exists and contains required variables."""
    if env_path is None:
        env_path = Path.cwd() / ".env"
    
    if not env_path.exists():
        return False
    
    try:
        with open(env_path, "r") as f:
            content = f.read()
            # Check for essential environment variables
            required_vars = ["DATABASE_URL", "API_KEY"]
            return any(var in content for var in required_vars)
    except Exception:
        return False


def check_database_connection(database_url: Optional[str] = None) -> bool:
    """Check if PostgreSQL database connection is available and properly formatted."""
    if not database_url:
        database_url = os.getenv("DATABASE_URL")
    
    if not database_url:
        return False
    
    # Check if the URL is properly formatted for PostgreSQL
    valid_prefixes = ("postgresql://", "postgres://")
    if not database_url.startswith(valid_prefixes):
        return False
    
    # Basic URL structure validation
    try:
        # Remove the protocol prefix
        url_without_protocol = database_url.split("://", 1)[1]
        
        # Check if it contains required components (user:password@host:port/database)
        if "@" not in url_without_protocol or "/" not in url_without_protocol:
            return False
        
        # Split into auth and host parts
        auth_part, host_part = url_without_protocol.split("@", 1)
        
        # Check auth part has user:password format
        if ":" not in auth_part:
            return False
        
        # Check host part has host:port/database format
        if "/" not in host_part:
            return False
        
        host_port, database = host_part.split("/", 1)
        
        # Check if database name is provided
        if not database.strip():
            return False
        
        return True
        
    except Exception:
        return False


def run_system_diagnostics(env_path: Optional[Path] = None) -> Dict[str, Any]:
    """Run comprehensive system diagnostics."""
    results = {
        "status": "unknown",
        "checks": {},
        "warnings": [],
        "errors": []
    }
    
    # Check environment configuration
    env_check = check_env_file(env_path)
    results["checks"]["environment"] = env_check
    if not env_check:
        results["warnings"].append("Environment file missing or incomplete")
    
    # Check database connection
    db_check = check_database_connection()
    results["checks"]["database"] = db_check
    if not db_check:
        results["warnings"].append("Database connection not configured")
    
    # Check service ports
    services = {
        "api": check_port("127.0.0.1", 8000),
        "frontend": check_port("127.0.0.1", 3000) or check_port("127.0.0.1", 5173),
        "dashboard": check_port("127.0.0.1", 8501)
    }
    results["checks"]["services"] = services
    
    # Determine overall status
    if all(results["checks"].values()) and all(services.values()):
        results["status"] = "healthy"
    elif any(results["checks"].values()) or any(services.values()):
        results["status"] = "partial"
    else:
        results["status"] = "unhealthy"
        results["errors"].append("No services are running")
    
    return results


def print_diagnostics_report(results: Dict[str, Any]) -> None:
    """Print a formatted diagnostics report."""
    print("=" * 60)
    print("AetherShelf System Diagnostics")
    print("=" * 60)
    
    status_icon = {
        "healthy": "✅",
        "partial": "⚠️",
        "unhealthy": "❌",
        "unknown": "❓"
    }
    
    print(f"Overall Status: {status_icon.get(results['status'], '❓')} {results['status'].upper()}")
    print()
    
    print("Service Checks:")
    for check, status in results["checks"].items():
        icon = "✅" if status else "❌"
        print(f"  {icon} {check.title()}: {'OK' if status else 'FAIL'}")
    
    if "services" in results["checks"]:
        print("\nService Ports:")
        for service, status in results["checks"]["services"].items():
            icon = "✅" if status else "❌"
            print(f"  {icon} {service.title()}: {'Running' if status else 'Stopped'}")
    
    if results["warnings"]:
        print("\nWarnings:")
        for warning in results["warnings"]:
            print(f"  ⚠️  {warning}")
    
    if results["errors"]:
        print("\nErrors:")
        for error in results["errors"]:
            print(f"  ❌ {error}")
    
    print("=" * 60)