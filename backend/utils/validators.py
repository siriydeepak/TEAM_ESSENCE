"""
Input validation and sanitization utilities.

This module provides common validation functions and utilities
for sanitizing and validating user input across the backend.
"""

import re
from typing import Optional, List, Dict, Any
from datetime import datetime, date
import logging

logger = logging.getLogger(__name__)

def validate_email(email: str) -> bool:
    """Validate email address format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_phone(phone: str) -> bool:
    """Validate phone number format."""
    # Remove all non-digit characters
    digits_only = re.sub(r'\D', '', phone)
    # Check if it's a valid length (10-15 digits)
    return 10 <= len(digits_only) <= 15

def sanitize_string(input_str: str, max_length: int = 255) -> str:
    """Sanitize string input by removing harmful characters."""
    if not isinstance(input_str, str):
        return ""
    
    # Remove potentially harmful characters
    sanitized = re.sub(r'[<>"\';\\]', '', input_str)
    
    # Trim whitespace and limit length
    sanitized = sanitized.strip()[:max_length]
    
    return sanitized

def validate_quantity(quantity: Any) -> Optional[float]:
    """Validate and convert quantity to float."""
    try:
        qty = float(quantity)
        if qty > 0:
            return qty
        else:
            logger.warning(f"Invalid quantity: {quantity} (must be positive)")
            return None
    except (ValueError, TypeError):
        logger.warning(f"Invalid quantity format: {quantity}")
        return None

def validate_date(date_str: str) -> Optional[date]:
    """Validate and parse date string."""
    try:
        # Try common date formats
        for fmt in ['%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y']:
            try:
                return datetime.strptime(date_str, fmt).date()
            except ValueError:
                continue
        
        logger.warning(f"Invalid date format: {date_str}")
        return None
    except Exception as e:
        logger.warning(f"Date validation error: {e}")
        return None

def validate_category(category: str) -> bool:
    """Validate inventory category."""
    valid_categories = [
        'fruits', 'vegetables', 'dairy', 'meat', 'seafood',
        'grains', 'beverages', 'snacks', 'condiments', 'frozen',
        'bakery', 'canned', 'other'
    ]
    return category.lower() in valid_categories

def validate_unit(unit: str) -> bool:
    """Validate measurement unit."""
    valid_units = [
        'kg', 'g', 'lb', 'oz', 'l', 'ml', 'gal', 'qt', 'pt',
        'cup', 'tbsp', 'tsp', 'piece', 'pack', 'bottle', 'can',
        'box', 'bag', 'bunch', 'dozen'
    ]
    return unit.lower() in valid_units

def sanitize_inventory_item(item_data: Dict[str, Any]) -> Dict[str, Any]:
    """Sanitize inventory item data."""
    sanitized = {}
    
    # Sanitize string fields
    if 'name' in item_data:
        sanitized['name'] = sanitize_string(item_data['name'], 255)
    
    if 'category' in item_data:
        sanitized['category'] = sanitize_string(item_data['category'], 100)
    
    if 'unit' in item_data:
        sanitized['unit'] = sanitize_string(item_data['unit'], 50)
    
    # Validate numeric fields
    if 'quantity' in item_data:
        qty = validate_quantity(item_data['quantity'])
        if qty is not None:
            sanitized['quantity'] = qty
    
    if 'price' in item_data and item_data['price'] is not None:
        price = validate_quantity(item_data['price'])
        if price is not None:
            sanitized['price'] = price
    
    if 'shelf_life_days' in item_data:
        try:
            shelf_life = int(item_data['shelf_life_days'])
            if shelf_life > 0:
                sanitized['shelf_life_days'] = shelf_life
        except (ValueError, TypeError):
            logger.warning(f"Invalid shelf_life_days: {item_data['shelf_life_days']}")
    
    # Validate date fields
    if 'purchase_date' in item_data:
        if isinstance(item_data['purchase_date'], str):
            parsed_date = validate_date(item_data['purchase_date'])
            if parsed_date:
                sanitized['purchase_date'] = parsed_date
        elif isinstance(item_data['purchase_date'], date):
            sanitized['purchase_date'] = item_data['purchase_date']
    
    return sanitized