"""
Inventory data models and schemas.

This module defines Pydantic models for inventory-related data structures,
including request/response schemas and database models.
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import date, datetime
from enum import Enum

class ItemStatus(str, Enum):
    """Enumeration for inventory item status."""
    GOOD = "good"
    WARNING = "warning"
    CRITICAL = "critical"
    EXPIRED = "expired"

class InventoryItemBase(BaseModel):
    """Base model for inventory items."""
    name: str = Field(..., min_length=1, max_length=255, description="Item name")
    category: str = Field(..., min_length=1, max_length=100, description="Item category")
    quantity: float = Field(..., gt=0, description="Item quantity")
    unit: str = Field(..., min_length=1, max_length=50, description="Unit of measurement")
    shelf_life_days: int = Field(..., gt=0, description="Shelf life in days")
    price: Optional[float] = Field(None, ge=0, description="Item price")

class InventoryItemCreate(InventoryItemBase):
    """Model for creating new inventory items."""
    purchase_date: Optional[date] = Field(default_factory=date.today, description="Purchase date")

class InventoryItemUpdate(BaseModel):
    """Model for updating inventory items."""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    category: Optional[str] = Field(None, min_length=1, max_length=100)
    quantity: Optional[float] = Field(None, gt=0)
    unit: Optional[str] = Field(None, min_length=1, max_length=50)
    shelf_life_days: Optional[int] = Field(None, gt=0)
    price: Optional[float] = Field(None, ge=0)

class InventoryItem(InventoryItemBase):
    """Complete inventory item model with computed fields."""
    id: str = Field(..., description="Unique item identifier")
    purchase_date: date = Field(..., description="Purchase date")
    expiry_date: date = Field(..., description="Calculated expiry date")
    days_left: int = Field(..., description="Days until expiry")
    status: ItemStatus = Field(..., description="Current item status")
    source: str = Field(default="manual", description="Source of item entry")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    @validator('status', always=True)
    def determine_status(cls, v, values):
        """Automatically determine item status based on days left."""
        days_left = values.get('days_left', 0)
        if days_left < 0:
            return ItemStatus.EXPIRED
        elif days_left <= 1:
            return ItemStatus.CRITICAL
        elif days_left <= 3:
            return ItemStatus.WARNING
        else:
            return ItemStatus.GOOD

class InventoryResponse(BaseModel):
    """Response model for inventory operations."""
    success: bool
    message: str
    data: Optional[InventoryItem] = None

class InventoryListResponse(BaseModel):
    """Response model for inventory list operations."""
    success: bool
    message: str
    data: List[InventoryItem] = []
    total: int = 0