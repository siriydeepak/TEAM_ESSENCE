"""
Receipt parsing and item extraction service.

This module contains the business logic for parsing receipts,
extracting items, and detecting collisions with existing inventory.
"""

import re
from typing import List, Dict, Any, Tuple
import logging

logger = logging.getLogger(__name__)

class ReceiptService:
    """Service class for receipt parsing and item extraction."""
    
    def __init__(self):
        """Initialize the receipt service."""
        self.platform_patterns = {
            "Blinkit": ["blinkit"],
            "Zepto": ["zepto"],
            "Amazon Fresh": ["amazon"],
            "BigBasket": ["bigbasket"],
            "Swiggy Instamart": ["swiggy"],
        }
    
    def detect_platform(self, receipt_text: str) -> str:
        """Detect the platform/service from receipt text."""
        text_lower = receipt_text.lower()
        
        for platform, patterns in self.platform_patterns.items():
            if any(pattern in text_lower for pattern in patterns):
                return platform
        
        return "Unknown"
    
    def extract_items(self, receipt_text: str, max_items: int = 10) -> List[Dict[str, Any]]:
        """
        Extract items from receipt text using regex patterns.
        
        Args:
            receipt_text: Raw receipt text content
            max_items: Maximum number of items to extract
            
        Returns:
            List of extracted items with name, quantity, and price
        """
        # Filter lines that likely contain items (have currency symbols or bullet points)
        lines = [
            line.strip() 
            for line in receipt_text.split('\n') 
            if re.search(r'₹|Rs\.|[-•*]', line) and line.strip()
        ]
        
        extracted_items = []
        
        for line in lines[:max_items]:
            item = self._parse_item_line(line)
            if item:
                extracted_items.append(item)
                logger.debug(f"Extracted item: {item}")
        
        logger.info(f"Extracted {len(extracted_items)} items from receipt")
        return extracted_items
    
    def _parse_item_line(self, line: str) -> Dict[str, Any]:
        """Parse a single line to extract item information."""
        # Extract item name (text after bullet point, before quantity or price)
        name_match = re.search(r'[-•*]\s*([A-Za-z\s]+?)(?:\s+x?\d|\s+₹|$)', line)
        if not name_match:
            return None
        
        item_name = name_match.group(1).strip()
        
        # Extract quantity (look for patterns like "x2", "2x", etc.)
        quantity_match = re.search(r'x(\d+)', line, re.IGNORECASE)
        quantity = int(quantity_match.group(1)) if quantity_match else 1
        
        # Extract price (look for ₹ or Rs. followed by numbers)
        price_match = re.search(r'(?:₹|Rs\.?)\s*(\d+(?:\.\d+)?)', line)
        price = float(price_match.group(1)) if price_match else None
        
        return {
            "name": item_name,
            "quantity": quantity,
            "price_inr": price,
            "raw_line": line
        }
    
    def detect_collisions(self, extracted_items: List[Dict[str, Any]], 
                         inventory_items: List[Dict[str, Any]]) -> List[str]:
        """
        Detect collisions between extracted items and existing inventory.
        
        Args:
            extracted_items: Items extracted from receipt
            inventory_items: Current inventory items
            
        Returns:
            List of collision alert messages
        """
        collision_alerts = []
        
        for new_item in extracted_items:
            # Use first word of item name as keyword for matching
            keyword = new_item["name"].lower().split()[0]
            
            # Find existing items with similar names that are still valid
            existing_item = self._find_similar_item(keyword, inventory_items)
            
            if existing_item and self._is_collision_worthy(existing_item):
                days_left = existing_item.get("days_left", 0)
                alert_message = (
                    f"Collision! You have {existing_item['name']} "
                    f"expiring in {days_left}d — do you need more?"
                )
                collision_alerts.append(alert_message)
                logger.info(f"Collision detected: {new_item['name']} vs {existing_item['name']}")
        
        return collision_alerts
    
    def _find_similar_item(self, keyword: str, inventory_items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Find inventory item with similar name using keyword matching."""
        for item in inventory_items:
            if (keyword in item["name"].lower() and 
                item.get("days_left", 99) >= 0):  # Item is not expired
                return item
        return None
    
    def _is_collision_worthy(self, existing_item: Dict[str, Any]) -> bool:
        """Determine if an existing item warrants a collision alert."""
        days_left = existing_item.get("days_left", 99)
        return days_left <= 5  # Alert if item expires within 5 days
    
    def generate_summary(self, extracted_items: List[Dict[str, Any]], 
                        platform: str, collision_alerts: List[str]) -> Dict[str, Any]:
        """Generate a summary of the receipt processing results."""
        total_items = len(extracted_items)
        total_value = sum(item.get("price_inr", 0) for item in extracted_items if item.get("price_inr"))
        
        return {
            "status": "ingested",
            "platform": platform,
            "extracted_items": extracted_items,
            "collision_alerts": collision_alerts,
            "summary": {
                "total_items": total_items,
                "total_value_inr": round(total_value, 2),
                "collisions_found": len(collision_alerts)
            },
            "message": f"Extracted {total_items} items from {platform}"
        }