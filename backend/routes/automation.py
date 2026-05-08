"""
Automation API routes.

This module contains API endpoints for automated inventory monitoring,
flux algorithm processing, and collision detection.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from ..services.automation_service import automation_service

router = APIRouter()

# Pydantic Models
class LocationCoordinates(BaseModel):
    lat: float
    lon: float

class AutomationRequest(BaseModel):
    location: LocationCoordinates
    inventory_items: Optional[List[Dict[str, Any]]] = None

class FluxCalculationRequest(BaseModel):
    temperature: float
    humidity: int

@router.post("/run-flux-check")
async def run_flux_check(request: AutomationRequest):
    """
    Run automated flux algorithm check on inventory with weather integration.
    
    This endpoint processes inventory items against current weather conditions
    and returns adjustments, collision alerts, and recommendations.
    """
    # Use provided inventory or get from default store
    inventory_items = request.inventory_items
    if not inventory_items:
        # Import default inventory (this will be replaced with service call)
        from .inventory import inventory_db
        inventory_items = inventory_db
    
    try:
        results = automation_service.run_automated_check(
            user_location={"lat": request.location.lat, "lon": request.location.lon},
            inventory_items=inventory_items
        )
        
        return {
            "status": "success",
            "results": results,
            "summary": {
                "total_items": results["items_processed"],
                "perishable_items": results["perishable_items"],
                "adjustments_made": len(results["adjustments"]),
                "collision_alerts": len(results["collision_alerts"]),
                "weather_penalty": f"{results['penalty_percentage']}%"
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Automation check failed: {str(e)}")

@router.post("/calculate-flux-penalty")
async def calculate_flux_penalty(request: FluxCalculationRequest):
    """
    Calculate flux penalty for given temperature and humidity.
    
    This endpoint allows testing the flux algorithm with specific weather conditions.
    """
    try:
        penalty = automation_service.calculate_decay_multiplier(
            request.temperature, 
            request.humidity
        )
        
        return {
            "temperature_celsius": request.temperature,
            "humidity_percentage": request.humidity,
            "penalty_fraction": penalty,
            "penalty_percentage": round(penalty * 100, 1),
            "algorithm": "Household Metabolist Flux Algorithm",
            "factors": {
                "temperature_impact": max(0, (request.temperature - 25) * 0.08),
                "humidity_impact": max(0, (int((request.humidity - 60) / 5)) * 0.03) if request.humidity > 60 else 0
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Calculation failed: {str(e)}")

@router.get("/collision-alerts/{user_id}")
async def get_collision_alerts(user_id: str):
    """
    Get current collision alerts for a user's inventory.
    
    This endpoint returns items that are at risk of spoiling based on
    current weather conditions.
    """
    # TODO: Implement user-specific inventory retrieval
    # For now, use default inventory
    from .inventory import inventory_db
    
    # Mock user location (this should come from user profile)
    user_location = {"lat": 13.0827, "lon": 80.2707}  # Chennai coordinates
    
    try:
        results = automation_service.run_automated_check(
            user_location=user_location,
            inventory_items=inventory_db
        )
        
        return {
            "user_id": user_id,
            "collision_alerts": results["collision_alerts"],
            "alert_count": len(results["collision_alerts"]),
            "weather_conditions": {
                "temperature": results["weather"]["temp"],
                "humidity": results["weather"]["humidity"],
                "city": results["weather"]["city"]
            },
            "generated_at": results["timestamp"]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get collision alerts: {str(e)}")

@router.post("/geocode")
async def geocode_city(city: str):
    """
    Convert city name to coordinates using geocoding service.
    
    This endpoint provides geocoding functionality for location-based features.
    """
    try:
        coordinates = automation_service.geocode_city(city)
        
        if not coordinates:
            raise HTTPException(status_code=404, detail=f"City '{city}' not found")
        
        return {
            "query": city,
            "result": coordinates,
            "status": "success"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Geocoding failed: {str(e)}")

@router.get("/algorithm-info")
async def get_algorithm_info():
    """
    Get detailed information about the Flux Algorithm and automation features.
    """
    return {
        "algorithm": {
            "name": "Household Metabolist Flux Algorithm",
            "version": "2.0",
            "description": "Weather-based shelf life adjustment system for perishable inventory items"
        },
        "factors": {
            "temperature": {
                "threshold": 25,
                "unit": "celsius",
                "impact": "8% penalty per degree above 25°C",
                "rationale": "Higher temperatures accelerate bacterial growth and spoilage"
            },
            "humidity": {
                "threshold": 60,
                "unit": "percentage",
                "impact": "3% penalty per 5% increase above 60%",
                "rationale": "High humidity promotes mold growth and moisture-related spoilage"
            }
        },
        "constraints": {
            "max_penalty": "60%",
            "min_adjustment": "0%",
            "perishable_categories": list(automation_service.PERISHABLE_CATEGORIES)
        },
        "features": [
            "Real-time weather integration",
            "Automated shelf life adjustments",
            "Collision detection for critical items",
            "Location-based processing",
            "Bulk inventory processing"
        ]
    }

@router.get("/health")
async def automation_health_check():
    """
    Health check for automation service functionality.
    """
    try:
        # Test weather API connectivity
        test_weather = automation_service.fetch_weather(13.0827, 80.2707)  # Chennai
        
        # Test flux calculation
        test_penalty = automation_service.calculate_decay_multiplier(30.0, 75)
        
        return {
            "status": "healthy",
            "service": "Automation Service",
            "weather_api": "connected" if test_weather.get("success") else "degraded",
            "flux_algorithm": "operational",
            "test_results": {
                "weather_fetch": test_weather.get("success", False),
                "penalty_calculation": test_penalty > 0,
                "geocoding": automation_service.geocode_city("Chennai") is not None
            }
        }
        
    except Exception as e:
        return {
            "status": "degraded",
            "service": "Automation Service",
            "error": str(e)
        }