"""
Weather service for OpenWeatherMap integration and flux algorithm.

This module contains the business logic for weather data retrieval,
geocoding, and shelf life adjustments based on weather conditions.
"""

import requests
from typing import Dict, Any, List, Tuple
import logging

logger = logging.getLogger(__name__)

class WeatherService:
    """Service class for weather operations and flux calculations."""
    
    def __init__(self, api_key: str):
        """Initialize the weather service with API key."""
        self.api_key = api_key
        self.base_geo_url = "http://api.openweathermap.org/geo/1.0/direct"
        self.base_weather_url = "https://api.openweathermap.org/data/2.5/weather"
    
    async def get_coordinates(self, city: str) -> Tuple[float, float, str]:
        """Get latitude, longitude, and formatted city name from city name."""
        geo_url = f"{self.base_geo_url}?q={city}&limit=1&appid={self.api_key}"
        
        try:
            response = requests.get(geo_url, timeout=5)
            response.raise_for_status()
            geo_data = response.json()
            
            if not geo_data:
                raise ValueError(f"City '{city}' not found")
            
            location = geo_data[0]
            lat = location["lat"]
            lon = location["lon"]
            city_name = f"{location['name']}, {location.get('country', '')}"
            
            logger.info(f"Geocoded {city} to {lat}, {lon}")
            return lat, lon, city_name
            
        except requests.RequestException as e:
            logger.error(f"Error geocoding city {city}: {e}")
            raise ValueError(f"Failed to geocode city: {e}")
    
    async def get_weather_data(self, lat: float, lon: float) -> Dict[str, Any]:
        """Get current weather data for given coordinates."""
        weather_url = f"{self.base_weather_url}?lat={lat}&lon={lon}&appid={self.api_key}&units=metric"
        
        try:
            response = requests.get(weather_url, timeout=5)
            response.raise_for_status()
            weather_data = response.json()
            
            return {
                "temperature": round(weather_data["main"]["temp"], 1),
                "humidity": weather_data["main"]["humidity"],
                "description": weather_data["weather"][0]["description"],
                "pressure": weather_data["main"]["pressure"],
                "feels_like": round(weather_data["main"]["feels_like"], 1)
            }
            
        except requests.RequestException as e:
            logger.error(f"Error fetching weather data for {lat}, {lon}: {e}")
            raise ValueError(f"Failed to fetch weather data: {e}")
    
    def calculate_flux_penalty(self, temperature: float, humidity: int) -> float:
        """
        Calculate shelf life decay multiplier based on weather conditions.
        
        Args:
            temperature: Temperature in Celsius
            humidity: Humidity percentage
            
        Returns:
            Penalty factor (0.0 to 0.6) representing shelf life reduction
        """
        penalty = 0.0
        
        # Temperature penalty: 8% per °C above 25°C
        if temperature > 25:
            penalty += (temperature - 25) * 0.08
        
        # Humidity penalty: 3% per 5% humidity above 60%
        if humidity > 60:
            penalty += ((humidity - 60) // 5) * 0.03
        
        # Cap penalty at 60%
        return min(penalty, 0.60)
    
    def apply_flux_to_inventory(self, inventory_items: List[Dict[str, Any]], 
                              penalty: float) -> List[Dict[str, Any]]:
        """
        Apply flux penalty to perishable inventory items.
        
        Args:
            inventory_items: List of inventory items
            penalty: Flux penalty factor (0.0 to 1.0)
            
        Returns:
            List of adjustments made to inventory items
        """
        perishable_categories = ["Dairy", "Protein", "Vegetables", "Bakery"]
        adjustments = []
        
        for item in inventory_items:
            if (item["category"] in perishable_categories and 
                item.get("days_left") is not None and 
                item["days_left"] > 0):
                
                original_days = item["days_left"]
                adjusted_days = max(0, int(original_days * (1 - penalty)))
                
                if adjusted_days < original_days:
                    item["days_left"] = adjusted_days
                    item["status"] = self._calculate_item_status(adjusted_days)
                    
                    adjustments.append({
                        "item": item["name"],
                        "original_days": original_days,
                        "adjusted_days": adjusted_days,
                        "reduction": original_days - adjusted_days
                    })
                    
                    logger.info(f"Applied flux to {item['name']}: {original_days} -> {adjusted_days} days")
        
        return adjustments
    
    def _calculate_item_status(self, days_left: int) -> str:
        """Calculate item status based on days left."""
        if days_left < 0: return "expired"
        if days_left == 0: return "urgent"
        if days_left <= 1: return "urgent"
        if days_left <= 3: return "critical"
        if days_left <= 7: return "warning"
        return "good"
    
    def is_weather_alert_needed(self, temperature: float, humidity: int) -> bool:
        """Determine if weather conditions warrant an alert."""
        return temperature > 28 or humidity > 70