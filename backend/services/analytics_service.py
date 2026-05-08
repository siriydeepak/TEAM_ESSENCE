"""
Analytics and reporting service.

This module contains the business logic for analytics calculations,
reporting, and data insights related to inventory management.
"""

from typing import List, Dict, Any
from datetime import datetime, date
import logging

logger = logging.getLogger(__name__)

class AnalyticsService:
    """Service class for analytics and reporting operations."""
    
    def __init__(self):
        """Initialize the analytics service."""
        pass
    
    def calculate_freshness_score(self, inventory_items: List[Dict[str, Any]]) -> int:
        """
        Calculate overall freshness score based on inventory status.
        
        Args:
            inventory_items: List of inventory items
            
        Returns:
            Freshness score (0-100)
        """
        if not inventory_items:
            return 100
        
        expired_count = len([
            item for item in inventory_items 
            if item.get("days_left") is not None and item["days_left"] < 0
        ])
        
        expiring_soon_count = len([
            item for item in inventory_items 
            if item.get("days_left") is not None and 0 <= item["days_left"] <= 3
        ])
        
        # Calculate score: start at 100, subtract penalties
        score = 100 - (expired_count * 20) - (expiring_soon_count * 8)
        return max(0, min(100, score))
    
    def categorize_inventory_by_status(self, inventory_items: List[Dict[str, Any]]) -> Dict[str, int]:
        """
        Categorize inventory items by their status.
        
        Args:
            inventory_items: List of inventory items
            
        Returns:
            Dictionary with counts for each status category
        """
        categories = {
            "total": len(inventory_items),
            "expired": 0,
            "expiring_soon": 0,
            "warning": 0,
            "healthy": 0,
            "unknown": 0
        }
        
        for item in inventory_items:
            days_left = item.get("days_left")
            
            if days_left is None:
                categories["unknown"] += 1
            elif days_left < 0:
                categories["expired"] += 1
            elif 0 <= days_left <= 3:
                categories["expiring_soon"] += 1
            elif 4 <= days_left <= 7:
                categories["warning"] += 1
            else:
                categories["healthy"] += 1
        
        return categories
    
    def calculate_waste_metrics(self, expiry_logs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculate waste-related metrics from expiry logs.
        
        Args:
            expiry_logs: List of expiry log entries
            
        Returns:
            Dictionary with waste metrics
        """
        total_waste_value = sum(
            log.get("waste_value", 0) 
            for log in expiry_logs 
            if log.get("action") in ["expired_discarded", "expired"]
        )
        
        waste_by_category = {}
        items_wasted = 0
        
        for log in expiry_logs:
            if log.get("action") in ["expired_discarded", "expired"]:
                category = log.get("category", "Unknown")
                waste_value = log.get("waste_value", 0)
                
                if category not in waste_by_category:
                    waste_by_category[category] = {"count": 0, "value": 0}
                
                waste_by_category[category]["count"] += 1
                waste_by_category[category]["value"] += waste_value
                items_wasted += 1
        
        return {
            "total_waste_value_inr": round(total_waste_value, 2),
            "items_wasted": items_wasted,
            "waste_by_category": waste_by_category,
            "average_waste_per_item": round(total_waste_value / max(items_wasted, 1), 2)
        }
    
    def calculate_savings_metrics(self, smart_cart_items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculate savings metrics from smart cart data.
        
        Args:
            smart_cart_items: List of smart cart items
            
        Returns:
            Dictionary with savings metrics
        """
        total_savings = sum(
            (item.get("original_price", 0) - item.get("best_price", 0))
            for item in smart_cart_items
        )
        
        approved_savings = sum(
            (item.get("original_price", 0) - item.get("best_price", 0))
            for item in smart_cart_items
            if item.get("approved", False)
        )
        
        pending_count = len([
            item for item in smart_cart_items 
            if not item.get("approved", False)
        ])
        
        return {
            "total_potential_savings_inr": round(total_savings, 2),
            "approved_savings_inr": round(approved_savings, 2),
            "pending_items": pending_count,
            "total_items": len(smart_cart_items)
        }
    
    def generate_comprehensive_summary(self, 
                                     inventory_items: List[Dict[str, Any]],
                                     expiry_logs: List[Dict[str, Any]],
                                     smart_cart_items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate a comprehensive analytics summary.
        
        Args:
            inventory_items: Current inventory items
            expiry_logs: Historical expiry logs
            smart_cart_items: Smart cart recommendations
            
        Returns:
            Comprehensive analytics summary
        """
        inventory_stats = self.categorize_inventory_by_status(inventory_items)
        freshness_score = self.calculate_freshness_score(inventory_items)
        waste_metrics = self.calculate_waste_metrics(expiry_logs)
        savings_metrics = self.calculate_savings_metrics(smart_cart_items)
        
        return {
            "inventory": inventory_stats,
            "freshness_score": freshness_score,
            "waste": waste_metrics,
            "savings": savings_metrics,
            "generated_at": datetime.now().isoformat()
        }
    
    def get_trending_categories(self, expiry_logs: List[Dict[str, Any]], 
                              days: int = 30) -> List[Dict[str, Any]]:
        """
        Get categories with highest waste in recent period.
        
        Args:
            expiry_logs: Historical expiry logs
            days: Number of days to look back
            
        Returns:
            List of categories sorted by waste value
        """
        cutoff_date = datetime.now().date() - timedelta(days=days)
        
        category_waste = {}
        
        for log in expiry_logs:
            log_date_str = log.get("date")
            if not log_date_str:
                continue
                
            try:
                log_date = datetime.strptime(log_date_str, "%Y-%m-%d").date()
                if log_date < cutoff_date:
                    continue
            except ValueError:
                continue
            
            if log.get("action") in ["expired_discarded", "expired"]:
                category = log.get("category", "Unknown")
                waste_value = log.get("waste_value", 0)
                
                if category not in category_waste:
                    category_waste[category] = {"count": 0, "value": 0}
                
                category_waste[category]["count"] += 1
                category_waste[category]["value"] += waste_value
        
        # Sort by waste value descending
        trending = [
            {"category": cat, **stats}
            for cat, stats in category_waste.items()
        ]
        
        return sorted(trending, key=lambda x: x["value"], reverse=True)