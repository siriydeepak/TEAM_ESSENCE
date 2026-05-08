"""
Database migration utilities for PostgreSQL.

This module provides utilities for migrating data and managing database schema
changes when transitioning from SQLite to PostgreSQL.
"""

import os
import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, date
from pathlib import Path

from .database import db_manager

logger = logging.getLogger(__name__)

class DatabaseMigration:
    """Database migration utilities for PostgreSQL."""
    
    def __init__(self):
        """Initialize migration utility."""
        self.db = db_manager
    
    async def export_sqlite_data(self, sqlite_path: str) -> Dict[str, List[Dict[str, Any]]]:
        """Export data from SQLite database to JSON format."""
        try:
            import sqlite3
            
            if not os.path.exists(sqlite_path):
                logger.warning(f"SQLite database not found at {sqlite_path}")
                return {}
            
            conn = sqlite3.connect(sqlite_path)
            conn.row_factory = sqlite3.Row  # Enable column access by name
            cursor = conn.cursor()
            
            exported_data = {}
            
            # Get all table names
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            
            for table in tables:
                table_name = table[0]
                if table_name.startswith('sqlite_'):
                    continue  # Skip SQLite system tables
                
                cursor.execute(f"SELECT * FROM {table_name}")
                rows = cursor.fetchall()
                
                # Convert rows to dictionaries
                exported_data[table_name] = []
                for row in rows:
                    row_dict = dict(row)
                    # Convert date/datetime objects to strings
                    for key, value in row_dict.items():
                        if isinstance(value, (date, datetime)):
                            row_dict[key] = value.isoformat()
                    exported_data[table_name].append(row_dict)
            
            conn.close()
            logger.info(f"Exported {len(exported_data)} tables from SQLite")
            return exported_data
            
        except ImportError:
            logger.error("sqlite3 module not available")
            return {}
        except Exception as e:
            logger.error(f"Failed to export SQLite data: {e}")
            return {}
    
    async def import_data_to_postgres(self, data: Dict[str, List[Dict[str, Any]]]) -> bool:
        """Import data from JSON format to PostgreSQL."""
        try:
            await self.db.initialize()
            
            if not self.db.use_postgres:
                logger.warning("PostgreSQL not available, cannot import data")
                return False
            
            success_count = 0
            total_count = 0
            
            for table_name, rows in data.items():
                if not rows:
                    continue
                
                logger.info(f"Importing {len(rows)} rows to table {table_name}")
                
                for row in rows:
                    total_count += 1
                    
                    if table_name == "inventory":
                        success = await self._import_inventory_row(row)
                    elif table_name == "expiry_logs":
                        success = await self._import_expiry_log_row(row)
                    elif table_name == "smart_cart":
                        success = await self._import_smart_cart_row(row)
                    elif table_name == "gap_suggestions":
                        success = await self._import_gap_suggestion_row(row)
                    else:
                        logger.warning(f"Unknown table: {table_name}")
                        continue
                    
                    if success:
                        success_count += 1
            
            logger.info(f"Successfully imported {success_count}/{total_count} rows")
            return success_count == total_count
            
        except Exception as e:
            logger.error(f"Failed to import data to PostgreSQL: {e}")
            return False
    
    async def _import_inventory_row(self, row: Dict[str, Any]) -> bool:
        """Import a single inventory row to PostgreSQL."""
        try:
            query = """
                INSERT INTO inventory (
                    id, name, category, quantity, unit, purchase_date, 
                    expiry_date, shelf_life_days, price, source, created_at, updated_at
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)
                ON CONFLICT (id) DO NOTHING
            """
            
            # Convert string dates back to date objects
            purchase_date = datetime.fromisoformat(row['purchase_date']).date() if isinstance(row['purchase_date'], str) else row['purchase_date']
            expiry_date = datetime.fromisoformat(row['expiry_date']).date() if isinstance(row['expiry_date'], str) else row['expiry_date']
            created_at = datetime.fromisoformat(row.get('created_at', datetime.utcnow().isoformat())) if isinstance(row.get('created_at'), str) else row.get('created_at', datetime.utcnow())
            updated_at = datetime.fromisoformat(row.get('updated_at', datetime.utcnow().isoformat())) if isinstance(row.get('updated_at'), str) else row.get('updated_at', datetime.utcnow())
            
            return await self.db.execute_command(
                query,
                row['id'],
                row['name'],
                row['category'],
                float(row['quantity']),
                row['unit'],
                purchase_date,
                expiry_date,
                int(row['shelf_life_days']),
                float(row['price']) if row.get('price') else None,
                row.get('source', 'manual'),
                created_at,
                updated_at
            )
            
        except Exception as e:
            logger.error(f"Failed to import inventory row: {e}")
            return False
    
    async def _import_expiry_log_row(self, row: Dict[str, Any]) -> bool:
        """Import a single expiry log row to PostgreSQL."""
        try:
            query = """
                INSERT INTO expiry_logs (
                    id, item_name, action, date, waste_value, category, created_at
                ) VALUES ($1, $2, $3, $4, $5, $6, $7)
                ON CONFLICT (id) DO NOTHING
            """
            
            log_date = datetime.fromisoformat(row['date']).date() if isinstance(row['date'], str) else row['date']
            created_at = datetime.fromisoformat(row.get('created_at', datetime.utcnow().isoformat())) if isinstance(row.get('created_at'), str) else row.get('created_at', datetime.utcnow())
            
            return await self.db.execute_command(
                query,
                row['id'],
                row['item_name'],
                row['action'],
                log_date,
                float(row.get('waste_value', 0)),
                row.get('category'),
                created_at
            )
            
        except Exception as e:
            logger.error(f"Failed to import expiry log row: {e}")
            return False
    
    async def _import_smart_cart_row(self, row: Dict[str, Any]) -> bool:
        """Import a single smart cart row to PostgreSQL."""
        try:
            query = """
                INSERT INTO smart_cart (
                    id, name, reason, urgency, best_price, original_price, 
                    source, savings_pct, approved, created_at
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
                ON CONFLICT (id) DO NOTHING
            """
            
            created_at = datetime.fromisoformat(row.get('created_at', datetime.utcnow().isoformat())) if isinstance(row.get('created_at'), str) else row.get('created_at', datetime.utcnow())
            
            return await self.db.execute_command(
                query,
                row['id'],
                row['name'],
                row['reason'],
                row['urgency'],
                float(row['best_price']),
                float(row['original_price']),
                row['source'],
                float(row['savings_pct']),
                bool(row.get('approved', False)),
                created_at
            )
            
        except Exception as e:
            logger.error(f"Failed to import smart cart row: {e}")
            return False
    
    async def _import_gap_suggestion_row(self, row: Dict[str, Any]) -> bool:
        """Import a single gap suggestion row to PostgreSQL."""
        try:
            query = """
                INSERT INTO gap_suggestions (
                    id, suggestion, missing_items, available_items, confidence, 
                    meals, category, cuisine, recipe, image_query, created_at
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
                ON CONFLICT (id) DO NOTHING
            """
            
            created_at = datetime.fromisoformat(row.get('created_at', datetime.utcnow().isoformat())) if isinstance(row.get('created_at'), str) else row.get('created_at', datetime.utcnow())
            
            return await self.db.execute_command(
                query,
                row['id'],
                row['suggestion'],
                row.get('missing_items', []),
                row.get('available_items', []),
                int(row['confidence']),
                int(row['meals']),
                row['category'],
                row['cuisine'],
                row.get('recipe'),
                row.get('image_query'),
                created_at
            )
            
        except Exception as e:
            logger.error(f"Failed to import gap suggestion row: {e}")
            return False
    
    async def migrate_from_sqlite(self, sqlite_path: str) -> bool:
        """Complete migration from SQLite to PostgreSQL."""
        try:
            logger.info(f"Starting migration from SQLite: {sqlite_path}")
            
            # Export data from SQLite
            data = await self.export_sqlite_data(sqlite_path)
            if not data:
                logger.warning("No data to migrate")
                return True
            
            # Import data to PostgreSQL
            success = await self.import_data_to_postgres(data)
            
            if success:
                logger.info("Migration completed successfully")
            else:
                logger.error("Migration completed with errors")
            
            return success
            
        except Exception as e:
            logger.error(f"Migration failed: {e}")
            return False
    
    async def backup_postgres_data(self, backup_path: str) -> bool:
        """Backup PostgreSQL data to JSON file."""
        try:
            await self.db.initialize()
            
            if not self.db.use_postgres:
                logger.warning("PostgreSQL not available, cannot backup")
                return False
            
            backup_data = {}
            
            # Backup inventory
            inventory_data = await self.db.execute_query("SELECT * FROM inventory ORDER BY created_at")
            backup_data['inventory'] = inventory_data
            
            # Backup expiry logs
            logs_data = await self.db.execute_query("SELECT * FROM expiry_logs ORDER BY created_at")
            backup_data['expiry_logs'] = logs_data
            
            # Backup smart cart
            cart_data = await self.db.execute_query("SELECT * FROM smart_cart ORDER BY created_at")
            backup_data['smart_cart'] = cart_data
            
            # Backup gap suggestions
            suggestions_data = await self.db.execute_query("SELECT * FROM gap_suggestions ORDER BY created_at")
            backup_data['gap_suggestions'] = suggestions_data
            
            # Write to file
            backup_file = Path(backup_path)
            backup_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(backup_file, 'w') as f:
                json.dump(backup_data, f, indent=2, default=str)
            
            logger.info(f"Backup completed: {backup_path}")
            return True
            
        except Exception as e:
            logger.error(f"Backup failed: {e}")
            return False

# Global migration instance
migration_manager = DatabaseMigration()