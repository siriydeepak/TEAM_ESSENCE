"""
Inventory management API routes.

This module contains all API endpoints related to inventory operations
including CRUD operations, search, and inventory analytics with PostgreSQL support.
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from datetime import datetime, timedelta
import uuid

from ..models.inventory import (
    InventoryItem, InventoryItemCreate, InventoryItemUpdate,
    InventoryResponse, InventoryListResponse
)
from ..services.inventory_service import InventoryService

router = APIRouter()

# Dependency to get inventory service
def get_inventory_service() -> InventoryService:
    return InventoryService()

@router.get("/", response_model=InventoryListResponse)
async def get_inventory(service: InventoryService = Depends(get_inventory_service)):
    """Get all inventory items from PostgreSQL."""
    try:
        items = await service.get_all_items()
        return InventoryListResponse(
            success=True,
            message=f"Retrieved {len(items)} inventory items",
            data=items,
            total=len(items)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve inventory: {str(e)}")

@router.get("/expiring", response_model=InventoryListResponse)
async def get_expiring(
    days: int = 3, 
    service: InventoryService = Depends(get_inventory_service)
):
    """Get items expiring within specified days."""
    try:
        if days < 0:
            raise HTTPException(status_code=400, detail="Days must be non-negative")
        
        items = await service.get_expiring_items(days)
        return InventoryListResponse(
            success=True,
            message=f"Found {len(items)} items expiring within {days} days",
            data=items,
            total=len(items)
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get expiring items: {str(e)}")

@router.get("/expired", response_model=InventoryListResponse)
async def get_expired(service: InventoryService = Depends(get_inventory_service)):
    """Get expired items."""
    try:
        items = await service.get_expired_items()
        return InventoryListResponse(
            success=True,
            message=f"Found {len(items)} expired items",
            data=items,
            total=len(items)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get expired items: {str(e)}")

@router.get("/search", response_model=InventoryListResponse)
async def search_inventory(
    q: str,
    service: InventoryService = Depends(get_inventory_service)
):
    """Search inventory items by name or category."""
    try:
        if not q or len(q.strip()) < 2:
            raise HTTPException(status_code=400, detail="Search query must be at least 2 characters")
        
        items = await service.search_items(q.strip())
        return InventoryListResponse(
            success=True,
            message=f"Found {len(items)} items matching '{q}'",
            data=items,
            total=len(items)
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to search inventory: {str(e)}")

@router.get("/{item_id}", response_model=InventoryResponse)
async def get_item(
    item_id: str,
    service: InventoryService = Depends(get_inventory_service)
):
    """Get a specific inventory item by ID."""
    try:
        item = await service.get_item_by_id(item_id)
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        
        return InventoryResponse(
            success=True,
            message="Item retrieved successfully",
            data=item
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get item: {str(e)}")

@router.post("/add", response_model=InventoryResponse)
async def add_item(
    item: InventoryItemCreate,
    service: InventoryService = Depends(get_inventory_service)
):
    """Add a new inventory item to PostgreSQL."""
    try:
        new_item = await service.add_item(item)
        if not new_item:
            raise HTTPException(status_code=500, detail="Failed to add item to database")
        
        return InventoryResponse(
            success=True,
            message="Item added successfully",
            data=new_item
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to add item: {str(e)}")

@router.put("/{item_id}", response_model=InventoryResponse)
async def update_item(
    item_id: str,
    item_update: InventoryItemUpdate,
    service: InventoryService = Depends(get_inventory_service)
):
    """Update an existing inventory item in PostgreSQL."""
    try:
        updated_item = await service.update_item(item_id, item_update)
        if not updated_item:
            raise HTTPException(status_code=404, detail="Item not found or update failed")
        
        return InventoryResponse(
            success=True,
            message="Item updated successfully",
            data=updated_item
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update item: {str(e)}")

@router.delete("/{item_id}")
async def delete_item(
    item_id: str,
    service: InventoryService = Depends(get_inventory_service)
):
    """Delete an inventory item from PostgreSQL."""
    try:
        success = await service.delete_item(item_id)
        if not success:
            raise HTTPException(status_code=404, detail="Item not found or delete failed")
        
        return {
            "success": True,
            "message": "Item deleted successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete item: {str(e)}")

# Legacy endpoint for backward compatibility
@router.post("/")
async def legacy_add_item(
    item: InventoryItemCreate,
    service: InventoryService = Depends(get_inventory_service)
):
    """Legacy endpoint for adding items (redirects to /add)."""
    return await add_item(item, service)