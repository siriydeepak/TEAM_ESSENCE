"""
Flux data models and schemas.

This module defines Pydantic models for flux engine calculations,
pantry entropy, and expiry monitoring.
"""

from pydantic import BaseModel, Field, validator
from typing import List, Dict, Optional, Any
from datetime import datetime, date
from enum import Enum


class ItemCategory(str, Enum):
    """Enumeration for item categories."""
    MILK = "Milk"
    VEGETABLES = "Vegetables"
    DRY_GOODS = "Dry Goods"


class ExpiryStatus(str, Enum):
    """Enumeration for expiry status."""
    FRESH = "fresh"
    EXPIRING_SOON = "expiring_soon"
    CRITICAL = "critical"
    EXPIRED = "expired"


class FluxItem(BaseModel):
    """Model for items in flux calculations."""
    name: str = Field(..., description="Item name")
    quantity: int = Field(..., ge=0, description="Item quantity")
    category: ItemCategory = Field(..., description="Item category")
    estimated_expiry: Optional[str] = Field(None, description="Estimated expiry date")
    days_remaining: int = Field(..., description="Days until expiry")
    status: ExpiryStatus = Field(..., description="Current expiry status")

    @validator('status', always=True)
    def determine_status(cls, v, values):
        """Automatically determine expiry status based on days remaining."""
        days_remaining = values.get('days_remaining', 0)
        if days_remaining < 0:
            return ExpiryStatus.EXPIRED
        elif days_remaining == 0:
            return ExpiryStatus.CRITICAL
        elif days_remaining <= 2:
            return ExpiryStatus.EXPIRING_SOON
        else:
            return ExpiryStatus.FRESH


class PantryEntropy(BaseModel):
    """Model for pantry entropy calculations."""
    total_items: int = Field(..., ge=0, description="Total number of items")
    active_items: int = Field(..., ge=0, description="Number of active (non-zero) items")
    expired_items: int = Field(..., ge=0, description="Number of expired items")
    average_days_remaining: float = Field(..., description="Average days remaining across all items")
    entropy_score: float = Field(..., description="Calculated entropy score")
    calculated_at: datetime = Field(default_factory=datetime.utcnow, description="Calculation timestamp")


class FluxTrigger(BaseModel):
    """Model for flux-based triggers."""
    trigger_type: str = Field(..., description="Type of trigger")
    target_skill: str = Field(..., description="Target skill to trigger")
    reason: str = Field(..., description="Reason for trigger")
    expiring_items: List[str] = Field(default_factory=list, description="Items causing the trigger")
    threshold_days: int = Field(default=2, description="Threshold for expiry trigger")


class FluxMonitoringResult(BaseModel):
    """Model for flux monitoring results."""
    pantry_entropy: PantryEntropy = Field(..., description="Current pantry entropy")
    expiring_items: List[FluxItem] = Field(default_factory=list, description="Items expiring soon")
    triggers: List[FluxTrigger] = Field(default_factory=list, description="Generated triggers")
    alerts_generated: int = Field(default=0, description="Number of alerts generated")
    actions_triggered: bool = Field(default=False, description="Whether actions were triggered")


class CategoryDecaySettings(BaseModel):
    """Model for category-specific decay settings."""
    category: ItemCategory = Field(..., description="Item category")
    default_days: int = Field(..., gt=0, description="Default decay days")
    keywords: List[str] = Field(..., description="Keywords for category identification")


class FluxConfiguration(BaseModel):
    """Model for flux engine configuration."""
    decay_settings: List[CategoryDecaySettings] = Field(..., description="Category decay settings")
    monitoring_interval: int = Field(default=1, description="Monitoring interval in seconds")
    trigger_threshold: int = Field(default=2, description="Days threshold for triggers")
    enable_auto_triggers: bool = Field(default=True, description="Enable automatic triggers")


class FluxEngineState(BaseModel):
    """Model for flux engine state."""
    running: bool = Field(default=False, description="Whether flux engine is running")
    last_check: Optional[datetime] = Field(None, description="Last monitoring check timestamp")
    items_processed: int = Field(default=0, description="Number of items processed")
    triggers_generated: int = Field(default=0, description="Number of triggers generated")
    configuration: FluxConfiguration = Field(..., description="Current configuration")


class ExpiryPrediction(BaseModel):
    """Model for expiry predictions."""
    item_name: str = Field(..., description="Item name")
    current_expiry: Optional[date] = Field(None, description="Current expiry date")
    predicted_expiry: date = Field(..., description="Predicted expiry date")
    confidence: float = Field(..., ge=0, le=1, description="Prediction confidence")
    factors: List[str] = Field(default_factory=list, description="Factors affecting prediction")


class FluxAnalytics(BaseModel):
    """Model for flux analytics and insights."""
    total_items_tracked: int = Field(default=0, description="Total items tracked")
    average_shelf_life: float = Field(default=0, description="Average shelf life across items")
    waste_prevention_score: float = Field(default=0, description="Waste prevention effectiveness")
    category_breakdown: Dict[str, int] = Field(default_factory=dict, description="Items by category")
    trend_analysis: Dict[str, Any] = Field(default_factory=dict, description="Trend analysis data")
    generated_at: datetime = Field(default_factory=datetime.utcnow, description="Analytics generation time")