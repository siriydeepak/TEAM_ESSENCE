"""
Weather integration API routes.

This module contains API endpoints for weather data integration
and shelf life adjustments based on weather conditions using the
automation service with the Flux Algorithm.
"""

from fastapi import APIRouter, HTTPException
from typing import Optional
from pydantic import BaseModel
import requests
from ..services.automation_service import automation_service

router = APIRouter()

# Pydantic Models
class LocationInput(BaseModel):
    city: str

class CoordinateInput(BaseModel):
    lat: float
    lon: float

@router.post("/location")
async def get_weather_by_city(loc: LocationInput):
    """
    Get weather data for a city and apply flux algorithm to inventory.
    Uses the automation service for comprehensive weather processing.
    """
    # Import inventory data (this will be replaced with service call)
    from .inventory import inventory_db
    
    # Step A: Geocoding
    coordinates = automation_service.geocode_city(loc.city)
    if not coordinates:
        raise HTTPException(status_code=404, detail="City not found")
    
    # Step B: Run automated check with weather integration
    results = automation_service.run_automated_check(
        user_location={"lat": coordinates["lat"], "lon": coordinates["lon"]},
        inventory_items=inventory_db
    )
    
    weather = results["weather"]
    
    return {
        "city": f"{coordinates['city']}, {weather.get('country', '')}" if weather.get('success') else coordinates['city'],
        "lat": coordinates["lat"], 
        "lon": coordinates["lon"],
        "temperature_celsius": weather["temp"],
        "humidity": weather["humidity"],
        "description": weather["description"],
        "flux_penalty_pct": results["penalty_percentage"],
        "alert": weather["temp"] > 28 or weather["humidity"] > 70,
        "adjustments": results["adjustments"],
        "collision_alerts": results["collision_alerts"],
        "items_processed": results["items_processed"],
        "perishable_items": results["perishable_items"]
    }

@router.post("/coordinates")
async def get_weather_by_coordinates(coords: CoordinateInput):
    """
    Get weather data for specific coordinates and apply flux algorithm.
    Direct coordinate input for more precise weather data.
    """
    # Import inventory data (this will be replaced with service call)
    from .inventory import inventory_db
    
    # Run automated check with weather integration
    results = automation_service.run_automated_check(
        user_location={"lat": coords.lat, "lon": coords.lon},
        inventory_items=inventory_db
    )
    
    weather = results["weather"]
    
    return {
        "lat": coords.lat,
        "lon": coords.lon,
        "city": weather.get("city", "Unknown"),
        "temperature_celsius": weather["temp"],
        "humidity": weather["humidity"],
        "description": weather["description"],
        "flux_penalty_pct": results["penalty_percentage"],
        "alert": weather["temp"] > 28 or weather["humidity"] > 70,
        "adjustments": results["adjustments"],
        "collision_alerts": results["collision_alerts"],
        "items_processed": results["items_processed"],
        "perishable_items": results["perishable_items"],
        "weather_success": weather.get("success", False)
    }

@router.get("/shelf-impact")
async def weather_shelf_impact_legacy():
    """Legacy endpoint — returns mock weather data for offline mode."""
    import random
    temp = round(30 + random.uniform(0, 8), 1)
    humidity = random.randint(65, 88)
    penalty = automation_service.calculate_decay_multiplier(temp, humidity)
    
    return {
        "temperature_celsius": temp, 
        "humidity": humidity,
        "alert": True, 
        "flux_penalty_pct": round(penalty * 100, 1),
        "message": f"⚠️ {temp}°C · {humidity}% humidity — shelf lives reduced by {round(penalty*100)}%",
        "adjustments": [
            {"item": "Amul Whole Milk", "original_days": 4, "adjusted_days": max(0, int(4*(1-penalty)))},
            {"item": "Baby Spinach", "original_days": 3, "adjusted_days": max(0, int(3*(1-penalty)))},
        ]
    }

@router.get("/flux-algorithm")
async def get_flux_algorithm_info():
    """
    Get information about the Flux Algorithm used for shelf life adjustments.
    """
    return {
        "algorithm": "Household Metabolist Flux Algorithm",
        "description": "Weather-based shelf life adjustment system",
        "factors": {
            "temperature": {
                "threshold": 25,
                "unit": "celsius",
                "penalty": "8% per degree above 25°C"
            },
            "humidity": {
                "threshold": 60,
                "unit": "percentage",
                "penalty": "3% per 5% increase above 60%"
            }
        },
        "max_penalty": "60%",
        "perishable_categories": list(automation_service.PERISHABLE_CATEGORIES),
        "version": "2.0"
    }