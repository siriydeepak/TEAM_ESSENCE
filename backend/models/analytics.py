"""
Analytics data models and schemas.

This module defines Pydantic models for analytics,
reporting, and data insights.
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime, date, timezone
from enum import Enum

class ExpiryAction(str, Enum):
    """Enumeration for expiry log actions."""
    EXPIRED_DISCARDED = "expired_discarded"
    EXPIRED = "expired"
    CONSUMED = "consumed"
    CONSUMED_BEFORE_EXPIRY = "consumed_before_expiry"

class ExpiryLog(BaseModel):
    """Model for expiry log entries."""
    id: str = Field(..., description="Unique log entry ID")
    item: str = Field(..., description="Item name")
    action: ExpiryAction = Field(..., description="Action taken")
    action_date: date = Field(..., description="Date of action")
    waste_value: float = Field(default=0, ge=0, description="Monetary value of waste")
    category: str = Field(..., description="Item category")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class InventoryStats(BaseModel):
    """Model for inventory statistics."""
    total: int = Field(default=0, description="Total items")
    expired: int = Field(default=0, description="Expired items")
    expiring_soon: int = Field(default=0, description="Items expiring soon")
    warning: int = Field(default=0, description="Items in warning state")
    healthy: int = Field(default=0, description="Healthy items")
    unknown: int = Field(default=0, description="Items with unknown status")

class WasteMetrics(BaseModel):
    """Model for waste-related metrics."""
    total_waste_value_inr: float = Field(default=0, description="Total waste value in INR")
    items_wasted: int = Field(default=0, description="Number of items wasted")
    waste_by_category: Dict[str, Dict[str, Any]] = Field(default_factory=dict, description="Waste breakdown by category")
    average_waste_per_item: float = Field(default=0, description="Average waste value per item")

class SavingsMetrics(BaseModel):
    """Model for savings-related metrics."""
    total_potential_savings_inr: float = Field(default=0, description="Total potential savings")
    approved_savings_inr: float = Field(default=0, description="Approved savings")
    pending_items: int = Field(default=0, description="Pending approval items")
    total_items: int = Field(default=0, description="Total smart cart items")

class AnalyticsSummary(BaseModel):
    """Model for comprehensive analytics summary."""
    inventory: InventoryStats = Field(default_factory=InventoryStats)
    freshness_score: int = Field(default=100, ge=0, le=100, description="Overall freshness score")
    waste: WasteMetrics = Field(default_factory=WasteMetrics)
    savings: SavingsMetrics = Field(default_factory=SavingsMetrics)
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class CategoryTrend(BaseModel):
    """Model for category trending data."""
    category: str = Field(..., description="Category name")
    count: int = Field(default=0, description="Number of items")
    value: float = Field(default=0, description="Total value")
    percentage: Optional[float] = Field(None, description="Percentage of total")