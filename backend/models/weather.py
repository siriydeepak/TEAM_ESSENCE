"""
Weather data models and schemas.

This module defines Pydantic models for weather-related data structures,
including API requests, responses, and flux calculations.
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class LocationInput(BaseModel):
    """Model for location input requests."""
    city: str = Field(..., min_length=1, max_length=100, description="City name")

class WeatherData(BaseModel):
    """Model for weather data response."""
    city: str = Field(..., description="City name with country")
    lat: float = Field(..., description="Latitude")
    lon: float = Field(..., description="Longitude")
    temperature_celsius: float = Field(..., description="Temperature in Celsius")
    humidity: int = Field(..., ge=0, le=100, description="Humidity percentage")
    description: str = Field(..., description="Weather description")
    pressure: Optional[int] = Field(None, description="Atmospheric pressure")
    feels_like: Optional[float] = Field(None, description="Feels like temperature")

class FluxAdjustment(BaseModel):
    """Model for individual flux adjustments."""
    item: str = Field(..., description="Item name")
    original_days: int = Field(..., description="Original days left")
    adjusted_days: int = Field(..., description="Adjusted days left")
    reduction: int = Field(..., description="Days reduced")

class WeatherFluxResponse(BaseModel):
    """Model for weather flux calculation response."""
    weather: WeatherData
    flux_penalty_pct: float = Field(..., ge=0, le=100, description="Flux penalty percentage")
    alert: bool = Field(..., description="Whether weather conditions warrant alert")
    adjustments: List[FluxAdjustment] = Field(default_factory=list, description="List of inventory adjustments")
    message: Optional[str] = Field(None, description="Additional message")

class MockWeatherResponse(BaseModel):
    """Model for mock weather data (offline mode)."""
    temperature_celsius: float
    humidity: int
    alert: bool
    flux_penalty_pct: float
    message: str
    adjustments: List[FluxAdjustment] = Field(default_factory=list)