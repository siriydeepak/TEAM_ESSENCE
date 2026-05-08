"""
System data models and schemas.

This module defines Pydantic models for system-related data structures,
including network status, diagnostics, and system events.
"""

from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum


class SystemStatus(str, Enum):
    """Enumeration for system status."""
    HEALTHY = "healthy"
    PARTIAL = "partial"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"


class ServiceStatus(BaseModel):
    """Model for individual service status."""
    name: str = Field(..., description="Service name")
    running: bool = Field(..., description="Whether service is running")
    port: Optional[int] = Field(None, description="Service port")
    url: Optional[str] = Field(None, description="Service URL")


class NetworkStatus(BaseModel):
    """Model for network status information."""
    local_ip: str = Field(..., description="Local IP address")
    local_url: str = Field(..., description="Local access URL")
    public_active: bool = Field(default=False, description="Public tunnel active")
    ngrok_active: bool = Field(default=False, description="Ngrok tunnel active")
    internet_available: bool = Field(default=True, description="Internet connectivity")
    heartbeat_active: bool = Field(default=True, description="System heartbeat active")


class SystemDiagnostics(BaseModel):
    """Model for system diagnostics results."""
    status: SystemStatus = Field(..., description="Overall system status")
    checks: Dict[str, bool] = Field(default_factory=dict, description="Individual check results")
    services: List[ServiceStatus] = Field(default_factory=list, description="Service status list")
    warnings: List[str] = Field(default_factory=list, description="System warnings")
    errors: List[str] = Field(default_factory=list, description="System errors")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Diagnostic timestamp")


class SystemEvent(BaseModel):
    """Model for system events."""
    id: str = Field(..., description="Event ID")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Event timestamp")
    event_type: str = Field(..., description="Type of event")
    message: str = Field(..., description="Event message")
    priority: str = Field(default="normal", description="Event priority")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional event data")


class AlertType(str, Enum):
    """Enumeration for alert types."""
    RESTOCK = "restock"
    COLLISION = "collision"
    UTILITY_GAP = "utility_gap"
    EXPIRY_WARNING = "expiry_warning"
    SYSTEM_ERROR = "system_error"


class SystemAlert(BaseModel):
    """Model for system alerts."""
    id: str = Field(..., description="Alert ID")
    type: AlertType = Field(..., description="Alert type")
    item: Optional[str] = Field(None, description="Related item name")
    message: str = Field(..., description="Alert message")
    priority: str = Field(default="normal", description="Alert priority")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Alert creation time")
    acknowledged: bool = Field(default=False, description="Whether alert is acknowledged")


class SystemState(BaseModel):
    """Model for complete system state."""
    status: SystemStatus = Field(..., description="System status")
    entropy_score: float = Field(default=0.0, description="Pantry entropy score")
    ledger: List[Dict[str, Any]] = Field(default_factory=list, description="Current inventory ledger")
    logs: str = Field(default="", description="Recent system logs")
    alerts: List[SystemAlert] = Field(default_factory=list, description="Active alerts")
    network: NetworkStatus = Field(..., description="Network status")
    last_updated: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")


class CloudSyncData(BaseModel):
    """Model for cloud synchronization data."""
    ledger: List[Dict[str, Any]] = Field(..., description="Inventory ledger data")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Sync timestamp")
    source: str = Field(default="remote", description="Data source")


class InventoryUpdateRequest(BaseModel):
    """Model for inventory update requests."""
    item_name: str = Field(..., min_length=1, description="Item name")
    quantity: int = Field(..., description="Quantity change")
    operation: str = Field(default="add", description="Operation type (add/remove)")


class PushSubscription(BaseModel):
    """Model for push notification subscriptions."""
    endpoint: str = Field(..., description="Push endpoint URL")
    keys: Dict[str, str] = Field(..., description="Push subscription keys")


class VapidKeyResponse(BaseModel):
    """Model for VAPID key response."""
    vapid_public_key: str = Field(..., description="VAPID public key")


class ApiResponse(BaseModel):
    """Generic API response model."""
    status: str = Field(..., description="Response status")
    message: str = Field(..., description="Response message")
    data: Optional[Any] = Field(None, description="Response data")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Response timestamp")