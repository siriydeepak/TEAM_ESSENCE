"""
Receipt parsing data models and schemas.

This module defines Pydantic models for receipt parsing,
item extraction, and collision detection.
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class ReceiptInput(BaseModel):
    """Model for receipt input requests."""
    content: str = Field(..., min_length=1, description="Raw receipt text content")
    source: str = Field(default="gmail", description="Source of receipt (gmail, sms, manual)")

class ExtractedItem(BaseModel):
    """Model for items extracted from receipts."""
    name: str = Field(..., description="Item name")
    quantity: int = Field(default=1, ge=1, description="Item quantity")
    price_inr: Optional[float] = Field(None, ge=0, description="Item price in INR")
    raw_line: Optional[str] = Field(None, description="Original line from receipt")

class ReceiptProcessingResult(BaseModel):
    """Model for receipt processing results."""
    status: str = Field(default="ingested", description="Processing status")
    platform: str = Field(..., description="Detected platform/service")
    source: str = Field(..., description="Receipt source")
    extracted_items: List[ExtractedItem] = Field(default_factory=list, description="Extracted items")
    collision_alerts: List[str] = Field(default_factory=list, description="Collision alert messages")
    summary: Dict[str, Any] = Field(default_factory=dict, description="Processing summary")
    message: str = Field(..., description="Processing result message")
    processed_at: datetime = Field(default_factory=datetime.utcnow, description="Processing timestamp")

class CollisionAlert(BaseModel):
    """Model for collision detection alerts."""
    new_item_name: str = Field(..., description="Name of new item from receipt")
    existing_item_name: str = Field(..., description="Name of existing inventory item")
    existing_days_left: int = Field(..., description="Days left for existing item")
    alert_message: str = Field(..., description="Human-readable alert message")
    severity: str = Field(default="warning", description="Alert severity level")