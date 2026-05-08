"""
Smart cart data models and schemas.

This module defines Pydantic models for smart cart functionality,
including price optimization and purchase recommendations.
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum

class UrgencyLevel(str, Enum):
    """Enumeration for urgency levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class SmartCartItemBase(BaseModel):
    """Base model for smart cart items."""
    name: str = Field(..., min_length=1, max_length=255, description="Item name")
    reason: str = Field(..., description="Reason for recommendation")
    urgency: UrgencyLevel = Field(..., description="Urgency level")
    best_price: float = Field(..., ge=0, description="Best available price")
    original_price: float = Field(..., ge=0, description="Original/regular price")
    source: str = Field(..., description="Source/platform for best price")

class SmartCartItemCreate(SmartCartItemBase):
    """Model for creating smart cart items."""
    pass

class SmartCartItem(SmartCartItemBase):
    """Complete smart cart item model."""
    id: str = Field(..., description="Unique item ID")
    savings_pct: float = Field(..., ge=0, le=100, description="Savings percentage")
    approved: bool = Field(default=False, description="Whether item is approved for purchase")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class CartApproval(BaseModel):
    """Model for cart item approval requests."""
    item_id: str = Field(..., description="Smart cart item ID")
    approved: bool = Field(..., description="Approval status")

class SmartCartResponse(BaseModel):
    """Model for smart cart API responses."""
    items: List[SmartCartItem] = Field(default_factory=list, description="Smart cart items")
    total_savings: float = Field(default=0, description="Total potential savings")
    pending_count: int = Field(default=0, description="Number of pending approvals")
    approved_count: int = Field(default=0, description="Number of approved items")

class PriceComparison(BaseModel):
    """Model for price comparison data."""
    platform: str = Field(..., description="Platform/source name")
    price: float = Field(..., ge=0, description="Price on this platform")
    availability: bool = Field(default=True, description="Item availability")
    delivery_time: Optional[str] = Field(None, description="Estimated delivery time")
    rating: Optional[float] = Field(None, ge=0, le=5, description="Platform rating")