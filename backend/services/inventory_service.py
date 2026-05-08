"""
Inventory business logic and data operations.

This module contains the core business logic for inventory management,
including data validation, processing, and PostgreSQL database operations.
"""

from typing import List, Optional, Dict, Any
from datetime import datetime, date, timedelta
import logging
import uuid

from ..utils.database import db_manager
from ..models.inventory import InventoryItem, InventoryItemCreate, InventoryItemUpdate

logger = logging.getLogger(__name__)

class InventoryService:
    """Service class for inventory management operations with PostgreSQL support."""
    
    def __init__(self):
        """Initialize the inventory service."""
        self.db = db_manager
    
    async def get_all_items(self) -> List[Dict[str, Any]]:
        """Retrieve all inventory items from PostgreSQL."""
        try:
            logger.info("Retrieving all inventory items")
            
            query = """
                SELECT 
                    id::text,
                    name,
                    category,
                    quantity,
                    unit,
                    purchase_date,
                    expiry_date,
                    shelf_life_days,
                    price,
                    source,
                    created_at,
                    updated_at,
                    EXTRACT(DAYS FROM (expiry_date - CURRENT_DATE))::int as days_left
                FROM inventory 
                ORDER BY expiry_date ASC
            """
            
            items = await self.db.execute_query(query)
            
            # Calculate status for each item
            for item in items:
                item['status'] = self._calculate_item_status(item.get('days_left', 0))
            
            return items
            
        except Exception as e:
            logger.error(f"Failed to retrieve inventory items: {e}")
            return []
    
    async def add_item(self, item_data: InventoryItemCreate) -> Optional[Dict[str, Any]]:
        """Add a new inventory item to PostgreSQL."""
        try:
            logger.info(f"Adding new inventory item: {item_data.name}")
            
            # Calculate expiry date
            purchase_date = item_data.purchase_date or date.today()
            expiry_date = purchase_date + timedelta(days=item_data.shelf_life_days)
            
            # Generate UUID for the item
            item_id = str(uuid.uuid4())
            
            query = """
                INSERT INTO inventory (
                    id, name, category, quantity, unit, purchase_date, 
                    expiry_date, shelf_life_days, price, source, created_at, updated_at
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)
                RETURNING id::text, name, category, quantity, unit, purchase_date, 
                         expiry_date, shelf_life_days, price, source, created_at, updated_at
            """
            
            now = datetime.utcnow()
            
            result = await self.db.fetch_one(
                query,
                item_id,
                item_data.name,
                item_data.category,
                float(item_data.quantity),
                item_data.unit,
                purchase_date,
                expiry_date,
                item_data.shelf_life_days,
                float(item_data.price) if item_data.price else None,
                "manual",
                now,
                now
            )
            
            if result:
                # Calculate days left and status
                days_left = (expiry_date - date.today()).days
                result['days_left'] = days_left
                result['status'] = self._calculate_item_status(days_left)
                
                logger.info(f"Successfully added inventory item: {item_data.name}")
                return result
            
            return None
            
        except Exception as e:
            logger.error(f"Failed to add inventory item: {e}")
            return None
    
    async def update_item(self, item_id: str, item_data: InventoryItemUpdate) -> Optional[Dict[str, Any]]:
        """Update an existing inventory item in PostgreSQL."""
        try:
            logger.info(f"Updating inventory item: {item_id}")
            
            # Build dynamic update query based on provided fields
            update_fields = []
            values = []
            param_count = 1
            
            if item_data.name is not None:
                update_fields.append(f"name = ${param_count}")
                values.append(item_data.name)
                param_count += 1
            
            if item_data.category is not None:
                update_fields.append(f"category = ${param_count}")
                values.append(item_data.category)
                param_count += 1
            
            if item_data.quantity is not None:
                update_fields.append(f"quantity = ${param_count}")
                values.append(float(item_data.quantity))
                param_count += 1
            
            if item_data.unit is not None:
                update_fields.append(f"unit = ${param_count}")
                values.append(item_data.unit)
                param_count += 1
            
            if item_data.shelf_life_days is not None:
                update_fields.append(f"shelf_life_days = ${param_count}")
                values.append(item_data.shelf_life_days)
                param_count += 1
                
                # Recalculate expiry date if shelf life changes
                update_fields.append(f"expiry_date = purchase_date + INTERVAL '{item_data.shelf_life_days} days'")
            
            if item_data.price is not None:
                update_fields.append(f"price = ${param_count}")
                values.append(float(item_data.price))
                param_count += 1
            
            if not update_fields:
                logger.warning("No fields to update")
                return None
            
            # Add updated_at timestamp
            update_fields.append(f"updated_at = ${param_count}")
            values.append(datetime.utcnow())
            param_count += 1
            
            # Add item_id for WHERE clause
            values.append(item_id)
            
            query = f"""
                UPDATE inventory 
                SET {', '.join(update_fields)}
                WHERE id = ${param_count}
                RETURNING id::text, name, category, quantity, unit, purchase_date, 
                         expiry_date, shelf_life_days, price, source, created_at, updated_at,
                         EXTRACT(DAYS FROM (expiry_date - CURRENT_DATE))::int as days_left
            """
            
            result = await self.db.fetch_one(query, *values)
            
            if result:
                result['status'] = self._calculate_item_status(result.get('days_left', 0))
                logger.info(f"Successfully updated inventory item: {item_id}")
                return result
            
            return None
            
        except Exception as e:
            logger.error(f"Failed to update inventory item: {e}")
            return None
    
    async def delete_item(self, item_id: str) -> bool:
        """Delete an inventory item from PostgreSQL."""
        try:
            logger.info(f"Deleting inventory item: {item_id}")
            
            query = "DELETE FROM inventory WHERE id = $1"
            success = await self.db.execute_command(query, item_id)
            
            if success:
                logger.info(f"Successfully deleted inventory item: {item_id}")
            
            return success
            
        except Exception as e:
            logger.error(f"Failed to delete inventory item: {e}")
            return False
    
    async def search_items(self, query: str) -> List[Dict[str, Any]]:
        """Search inventory items by name or category using PostgreSQL full-text search."""
        try:
            logger.info(f"Searching inventory items: {query}")
            
            search_query = """
                SELECT 
                    id::text,
                    name,
                    category,
                    quantity,
                    unit,
                    purchase_date,
                    expiry_date,
                    shelf_life_days,
                    price,
                    source,
                    created_at,
                    updated_at,
                    EXTRACT(DAYS FROM (expiry_date - CURRENT_DATE))::int as days_left
                FROM inventory 
                WHERE 
                    name ILIKE $1 OR 
                    category ILIKE $1
                ORDER BY 
                    CASE 
                        WHEN name ILIKE $1 THEN 1 
                        ELSE 2 
                    END,
                    expiry_date ASC
            """
            
            search_pattern = f"%{query}%"
            items = await self.db.execute_query(search_query, search_pattern)
            
            # Calculate status for each item
            for item in items:
                item['status'] = self._calculate_item_status(item.get('days_left', 0))
            
            return items
            
        except Exception as e:
            logger.error(f"Failed to search inventory items: {e}")
            return []
    
    async def get_expiring_items(self, days: int = 3) -> List[Dict[str, Any]]:
        """Get items expiring within specified days using PostgreSQL date functions."""
        try:
            logger.info(f"Getting items expiring within {days} days")
            
            query = """
                SELECT 
                    id::text,
                    name,
                    category,
                    quantity,
                    unit,
                    purchase_date,
                    expiry_date,
                    shelf_life_days,
                    price,
                    source,
                    created_at,
                    updated_at,
                    EXTRACT(DAYS FROM (expiry_date - CURRENT_DATE))::int as days_left
                FROM inventory 
                WHERE expiry_date BETWEEN CURRENT_DATE AND CURRENT_DATE + INTERVAL '%s days'
                ORDER BY expiry_date ASC
            """ % days
            
            items = await self.db.execute_query(query)
            
            # Calculate status for each item
            for item in items:
                item['status'] = self._calculate_item_status(item.get('days_left', 0))
            
            return items
            
        except Exception as e:
            logger.error(f"Failed to get expiring items: {e}")
            return []
    
    async def get_expired_items(self) -> List[Dict[str, Any]]:
        """Get expired items using PostgreSQL date functions."""
        try:
            logger.info("Getting expired items")
            
            query = """
                SELECT 
                    id::text,
                    name,
                    category,
                    quantity,
                    unit,
                    purchase_date,
                    expiry_date,
                    shelf_life_days,
                    price,
                    source,
                    created_at,
                    updated_at,
                    EXTRACT(DAYS FROM (expiry_date - CURRENT_DATE))::int as days_left
                FROM inventory 
                WHERE expiry_date < CURRENT_DATE
                ORDER BY expiry_date DESC
            """
            
            items = await self.db.execute_query(query)
            
            # Calculate status for each item
            for item in items:
                item['status'] = self._calculate_item_status(item.get('days_left', 0))
            
            return items
            
        except Exception as e:
            logger.error(f"Failed to get expired items: {e}")
            return []
    
    async def get_item_by_id(self, item_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific inventory item by ID."""
        try:
            logger.info(f"Getting inventory item by ID: {item_id}")
            
            query = """
                SELECT 
                    id::text,
                    name,
                    category,
                    quantity,
                    unit,
                    purchase_date,
                    expiry_date,
                    shelf_life_days,
                    price,
                    source,
                    created_at,
                    updated_at,
                    EXTRACT(DAYS FROM (expiry_date - CURRENT_DATE))::int as days_left
                FROM inventory 
                WHERE id = $1
            """
            
            item = await self.db.fetch_one(query, item_id)
            
            if item:
                item['status'] = self._calculate_item_status(item.get('days_left', 0))
            
            return item
            
        except Exception as e:
            logger.error(f"Failed to get inventory item by ID: {e}")
            return None
    
    def _calculate_item_status(self, days_left: int) -> str:
        """Calculate item status based on days left until expiry."""
        if days_left < 0:
            return "expired"
        elif days_left == 0:
            return "critical"
        elif days_left <= 1:
            return "critical"
        elif days_left <= 3:
            return "warning"
        else:
            return "good"