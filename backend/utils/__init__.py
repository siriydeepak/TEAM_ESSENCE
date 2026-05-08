"""
Backend utilities package.
Contains utility functions for inventory management, parsing, security, and system monitoring.
"""

from .database import *
from .validators import *
from .flux_engine import *
from .gap_finder import *
from .email_parser import *
from .ledger_handler import *
from .network_check import *
from .security import *
from .system_check import *
from .events import *

__all__ = [
    # Database utilities
    "get_database_connection",
    "create_tables",
    "migrate_database",
    
    # Validators
    "validate_inventory_item",
    "validate_receipt_data",
    "validate_weather_data",
    
    # Flux engine
    "parse_expiry",
    "categorize_item",
    "get_decay_days",
    "calculate_days_remaining",
    "calculate_pantry_entropy",
    "find_expiring_items",
    
    # Gap finder
    "find_expiring_items",
    "generate_recipe_suggestions",
    "call_gemini_suggestion",
    
    # Email parser
    "extract_items_from_receipt",
    "parse_receipts",
    "call_gemini_parse_api",
    
    # Ledger handler
    "load_ledger",
    "save_ledger",
    "get_inventory",
    "get_item",
    "add_item",
    "remove_item",
    "update_inventory",
    
    # Network check
    "get_local_ip",
    "check_ngrok_status",
    "check_port",
    "check_internet_connectivity",
    "get_network_status",
    
    # Security
    "sanitize_ocr_input",
    "sanitize_item_name",
    "sanitize_api_key",
    "validate_quantity",
    "validate_email_format",
    "SecureClawAuth",
    
    # System check
    "check_env_file",
    "check_database_connection",
    "run_system_diagnostics",
    "print_diagnostics_report",
    
    # Events
    "notify_user",
    "log_inventory_event",
    "log_api_event",
    "create_system_event",
    "format_alert_message",
]