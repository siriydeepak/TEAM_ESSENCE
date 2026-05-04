import re

def sanitize_ocr_input(text: str) -> str:
    """Sanitizes text to prevent prompt injection and maintain benign code status."""
    if not text:
        return ""
    # Allow alphanumeric, spaces, and basic punctuation
    return re.sub(r"[^a-zA-Z0-9\s.,-]", "", str(text))

class SecureClawAuth:
    @staticmethod
    def sanitize_key(key: str) -> str:
        """Strips invalid characters from API keys."""
        if not key:
            return ""
        return re.sub(r"[^a-zA-Z0-9_\-]", "", str(key))
