"""
Automation Service for AetherShelf Backend

This service contains the automation engine functionality including:
- Weather-based shelf life adjustments (Flux Algorithm)
- Pantry collision detection
- Automated inventory monitoring
- Environmental factor processing

Migrated from TEAM_ESSENCE/backend/automation_engine.py
"""

import os
import logging
from datetime import datetime, timezone, timedelta
from typing import Optional, Dict, List, Any
import requests

# Configure logging
logger = logging.getLogger(__name__)

# Configuration
OWM_API_KEY = os.getenv("OWM_API_KEY", "86a9711ca833b672b3cc7cf70400535c")
PERISHABLE_CATEGORIES = {"Dairy", "Protein", "Vegetables", "Bakery", "Fruits"}

class AutomationService:
    """Service for automated inventory monitoring and weather-based adjustments."""
    
    def __init__(self):
        self.owm_api_key = OWM_API_KEY
        
    def fetch_weather(self, lat: float, lon: float) -> Dict[str, Any]:
        """
        Fetch current weather data for given coordinates.
        
        Args:
            lat: Latitude
            lon: Longitude
            
        Returns:
            Dictionary containing temperature, humidity, and description
        """
        url = (
            f"https://api.openweathermap.org/data/2.5/weather"
            f"?lat={lat}&lon={lon}&appid={self.owm_api_key}&units=metric"
        )
        
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            return {
                "temp": round(data["main"]["temp"], 1),
                "humidity": data["main"]["humidity"],
                "description": data["weather"][0]["description"],
                "city": data.get("name", ""),
                "success": True
            }
        except Exception as exc:
            logger.error(f"OpenWeatherMap error for ({lat},{lon}): {exc}")
            return {
                "temp": 30.0, 
                "humidity": 75, 
                "description": "simulated", 
                "city": "unknown",
                "success": False,
                "error": str(exc)
            }
    
    def geocode_city(self, city: str) -> Optional[Dict[str, Any]]:
        """
        Convert city name to coordinates using OpenWeatherMap Geocoding API.
        
        Args:
            city: City name
            
        Returns:
            Dictionary with lat, lon, and city name or None if not found
        """
        url = (
            f"http://api.openweathermap.org/geo/1.0/direct"
            f"?q={city}&limit=1&appid={self.owm_api_key}"
        )
        
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data:
                return {
                    "lat": data[0]["lat"], 
                    "lon": data[0]["lon"], 
                    "city": data[0]["name"]
                }
        except Exception as exc:
            logger.error(f"Geocoding error for '{city}': {exc}")
        
        return None
    
    def calculate_decay_multiplier(self, temp: float, humidity: int) -> float:
        """
        Calculate shelf life decay multiplier based on environmental factors.
        
        Household Metabolist Flux Algorithm:
        - Temperature > 25°C: -8% per degree above 25
        - Humidity > 60%: -3% per 5% increase above 60
        
        Args:
            temp: Temperature in Celsius
            humidity: Humidity percentage
            
        Returns:
            Penalty fraction (0.0 - 0.60)
        """
        penalty = 0.0
        
        if temp > 25:
            penalty += (temp - 25) * 0.08
            
        if humidity > 60:
            penalty += (int((humidity - 60) / 5)) * 0.03
            
        return round(min(penalty, 0.60), 4)
    
    def calculate_adjusted_days(self, expiry_date: datetime, penalty: float) -> float:
        """
        Calculate adjusted days left after applying weather penalty.
        
        Args:
            expiry_date: Original expiry date
            penalty: Weather penalty fraction
            
        Returns:
            Adjusted days left
        """
        now = datetime.now(timezone.utc)
        
        # Ensure expiry_date is timezone-aware
        if expiry_date.tzinfo is None:
            expiry_date = expiry_date.replace(tzinfo=timezone.utc)
            
        base_days_left = (expiry_date - now).total_seconds() / 86400
        
        if base_days_left <= 0:
            return 0.0
            
        return round(base_days_left * (1 - penalty), 2)
    
    def generate_collision_alert(self, item: Dict[str, Any], adjusted_days: float) -> Dict[str, Any]:
        """
        Generate a pantry collision alert for critical items.
        
        Args:
            item: Inventory item dictionary
            adjusted_days: Adjusted days left
            
        Returns:
            Alert dictionary
        """
        return {
            "alert_type": "PANTRY_COLLISION",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "item_id": str(item.get("id", "")),
            "product_name": item.get("name", "Unknown"),
            "category": item.get("category", ""),
            "adjusted_days_left": adjusted_days,
            "message": (
                f"⚠ CRITICAL: {item.get('name')} will spoil in "
                f"{adjusted_days:.1f} day(s) due to current weather conditions. "
                f"Use it today!"
            ),
            "recommended_action": "consume_immediately" if adjusted_days < 0.5 else "consume_today"
        }
    
    def process_inventory_flux(self, inventory_items: List[Dict[str, Any]], 
                              weather_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process inventory items and apply flux algorithm based on weather.
        
        Args:
            inventory_items: List of inventory items
            weather_data: Weather data dictionary
            
        Returns:
            Processing results with adjustments and alerts
        """
        temp = weather_data.get("temp", 25.0)
        humidity = weather_data.get("humidity", 60)
        penalty = self.calculate_decay_multiplier(temp, humidity)
        
        adjustments = []
        collision_alerts = []
        
        for item in inventory_items:
            # Only process perishable items
            if item.get("category") not in PERISHABLE_CATEGORIES:
                continue
                
            # Parse expiry date
            expiry_str = item.get("expiry_date")
            if not expiry_str:
                continue
                
            try:
                if isinstance(expiry_str, str):
                    expiry_date = datetime.fromisoformat(expiry_str.replace("Z", "+00:00"))
                else:
                    expiry_date = expiry_str
                    
                original_days = item.get("days_left", 0)
                adjusted_days = self.calculate_adjusted_days(expiry_date, penalty)
                
                # Update item with adjusted values
                item["days_left"] = max(0, int(adjusted_days))
                item["status"] = self._calculate_item_status(item["days_left"])
                
                if adjusted_days < original_days:
                    adjustments.append({
                        "item": item["name"],
                        "original_days": original_days,
                        "adjusted_days": adjusted_days,
                        "penalty_applied": penalty
                    })
                
                # Generate collision alert for critical items
                if adjusted_days < 1.0:
                    alert = self.generate_collision_alert(item, adjusted_days)
                    collision_alerts.append(alert)
                    
            except Exception as e:
                logger.error(f"Error processing item {item.get('name')}: {e}")
                continue
        
        return {
            "weather": weather_data,
            "penalty_applied": penalty,
            "penalty_percentage": round(penalty * 100, 1),
            "adjustments": adjustments,
            "collision_alerts": collision_alerts,
            "items_processed": len(inventory_items),
            "perishable_items": len([i for i in inventory_items if i.get("category") in PERISHABLE_CATEGORIES])
        }
    
    def _calculate_item_status(self, days_left: int) -> str:
        """Calculate item status based on days left."""
        if days_left < 0:
            return "expired"
        elif days_left == 0:
            return "urgent"
        elif days_left <= 1:
            return "urgent"
        elif days_left <= 3:
            return "critical"
        elif days_left <= 7:
            return "warning"
        else:
            return "good"
    
    def run_automated_check(self, user_location: Dict[str, float], 
                           inventory_items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Run automated inventory check with weather integration.
        
        Args:
            user_location: Dictionary with 'lat' and 'lon' keys
            inventory_items: List of inventory items to process
            
        Returns:
            Complete processing results
        """
        # Fetch weather data
        weather_data = self.fetch_weather(
            user_location["lat"], 
            user_location["lon"]
        )
        
        if not weather_data.get("success", False):
            logger.warning("Weather fetch failed, using default values")
            weather_data = {
                "temp": 25.0,
                "humidity": 60,
                "description": "default",
                "city": "unknown",
                "success": False
            }
        
        # Process inventory with flux algorithm
        results = self.process_inventory_flux(inventory_items, weather_data)
        
        # Add metadata
        results["timestamp"] = datetime.now(timezone.utc).isoformat()
        results["location"] = user_location
        
        return results

# Global service instance
automation_service = AutomationService()