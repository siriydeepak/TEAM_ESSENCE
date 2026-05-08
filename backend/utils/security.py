"""
Security - Input sanitization and authentication utilities.
Handles secure input processing and API key management.
"""
import re
from typing import Optional


def sanitize_ocr_input(text: str) -> str:
    """Sanitizes text to prevent prompt injection and maintain benign code status."""
    if not text:
        return ""
    # Allow alphanumeric, spaces, and basic punctuation
    return re.sub(r"[^a-zA-Z0-9\s.,-]", "", str(text))


def sanitize_item_name(name: str) -> str:
    """Sanitize item name for safe storage and processing."""
    if not name:
        return ""
    # Allow alphanumeric, spaces, and common food-related characters
    return re.sub(r"[^a-zA-Z0-9\s.,-()&']", "", str(name)).strip()


def sanitize_api_key(key: str) -> str:
    """Strips invalid characters from API keys."""
    if not key:
        return ""
    return re.sub(r"[^a-zA-Z0-9_\-]", "", str(key))


def validate_quantity(quantity: str) -> Optional[int]:
    """Validate and convert quantity string to integer."""
    try:
        qty = int(str(quantity).strip())
        return qty if qty >= 0 else None
    except (ValueError, TypeError):
        return None


def validate_email_format(email: str) -> bool:
    """Basic email format validation."""
    if not email:
        return False
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


class SecureClawAuth:
    """Authentication utilities for secure API access."""
    
    @staticmethod
    def sanitize_key(key: str) -> str:
        """Strips invalid characters from API keys."""
        return sanitize_api_key(key)
    
    @staticmethod
    def validate_bearer_token(token: str, expected_token: str) -> bool:
        """Validate bearer token for API authentication."""
        if not token or not expected_token:
            return False
        return token.strip() == expected_token.strip()
    
    @staticmethod
    def generate_safe_session_id() -> str:
        """Generate a safe session identifier."""
        import secrets
        return secrets.token_urlsafe(32)