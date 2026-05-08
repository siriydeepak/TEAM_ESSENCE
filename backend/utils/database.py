"""
Database connection and utility functions.

This module provides PostgreSQL database connection management and common
database operations for the backend services with fallback to in-memory storage.
"""

import os
import asyncio
import logging
import uuid
from typing import Optional, Dict, Any, List, Union
from contextlib import asynccontextmanager
from datetime import datetime, date

logger = logging.getLogger(__name__)

class DatabaseManager:
    """PostgreSQL database connection and operations manager with in-memory fallback."""
    
    def __init__(self):
        """Initialize database manager."""
        self.connection_pool = None
        self.database_url = os.getenv("DATABASE_URL")
        self.use_postgres = bool(self.database_url)
        self.memory_store = None
        self._initialized = False
        
    async def initialize(self):
        """Initialize database connection."""
        if self._initialized:
            return
            
        if self.use_postgres:
            await self._initialize_postgres()
        else:
            await self._initialize_fallback()
        
        self._initialized = True
    
    async def _initialize_postgres(self):
        """Initialize PostgreSQL connection pool with proper configuration."""
        try:
            import asyncpg
            
            # Create connection pool with optimized settings for Vercel
            self.connection_pool = await asyncpg.create_pool(
                self.database_url,
                min_size=1,
                max_size=20,  # Increased for better concurrency
                command_timeout=30,  # Reduced timeout for serverless
                server_settings={
                    'application_name': 'aethershelf_backend',
                    'jit': 'off'  # Disable JIT for faster cold starts
                }
            )
            
            # Test connection and create tables if needed
            async with self.connection_pool.acquire() as conn:
                await self._create_tables_if_not_exist(conn)
            
            logger.info("PostgreSQL connection pool initialized successfully")
            self.use_postgres = True
            
        except ImportError:
            logger.error("asyncpg not installed, falling back to in-memory storage")
            await self._initialize_fallback()
        except Exception as e:
            logger.error(f"Failed to initialize PostgreSQL: {e}")
            await self._initialize_fallback()
    
    async def _create_tables_if_not_exist(self, conn):
        """Create database tables if they don't exist."""
        try:
            # Inventory table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS inventory (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    name VARCHAR(255) NOT NULL,
                    category VARCHAR(100) NOT NULL,
                    quantity DECIMAL(10,2) NOT NULL,
                    unit VARCHAR(50) NOT NULL,
                    purchase_date DATE NOT NULL,
                    expiry_date DATE NOT NULL,
                    shelf_life_days INTEGER NOT NULL,
                    price DECIMAL(10,2),
                    source VARCHAR(255) DEFAULT 'manual',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            
            # Expiry logs table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS expiry_logs (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    item_name VARCHAR(255) NOT NULL,
                    action VARCHAR(100) NOT NULL,
                    date DATE NOT NULL,
                    waste_value DECIMAL(10,2) DEFAULT 0,
                    category VARCHAR(100),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            
            # Smart cart table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS smart_cart (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    name VARCHAR(255) NOT NULL,
                    reason TEXT NOT NULL,
                    urgency VARCHAR(50) NOT NULL,
                    best_price DECIMAL(10,2) NOT NULL,
                    original_price DECIMAL(10,2) NOT NULL,
                    source VARCHAR(255) NOT NULL,
                    savings_pct DECIMAL(5,2) NOT NULL,
                    approved BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            
            # Gap finder suggestions table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS gap_suggestions (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    suggestion VARCHAR(255) NOT NULL,
                    missing_items TEXT[] NOT NULL,
                    available_items TEXT[] NOT NULL,
                    confidence INTEGER NOT NULL,
                    meals INTEGER NOT NULL,
                    category VARCHAR(100) NOT NULL,
                    cuisine VARCHAR(100) NOT NULL,
                    recipe TEXT,
                    image_query VARCHAR(255),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            
            # Telegram links table (Aether-Link Protocol)
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS telegram_links (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    web_user_id VARCHAR(255) NOT NULL UNIQUE,
                    telegram_user_id BIGINT NOT NULL,
                    chat_id BIGINT NOT NULL,
                    linked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_notified_at TIMESTAMP,
                    active BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            
            # Create indexes for better performance
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_inventory_expiry_date ON inventory(expiry_date);")
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_inventory_category ON inventory(category);")
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_expiry_logs_date ON expiry_logs(date);")
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_telegram_links_web_user ON telegram_links(web_user_id);")
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_telegram_links_telegram_user ON telegram_links(telegram_user_id);")
            
            logger.info("Database tables created/verified successfully")
            
        except Exception as e:
            logger.error(f"Failed to create database tables: {e}")
            raise
    
    async def _initialize_fallback(self):
        """Initialize fallback in-memory storage with sample data."""
        logger.warning("Using in-memory storage fallback")
        self.use_postgres = False
        
        # Initialize with sample data for development
        self.memory_store = {
            "inventory": [
                {
                    "id": "1",
                    "name": "Amul Whole Milk",
                    "category": "Dairy",
                    "quantity": 1.5,
                    "unit": "L",
                    "purchase_date": "2025-05-03",
                    "expiry_date": "2025-05-07",
                    "shelf_life_days": 7,
                    "price": 62.0,
                    "source": "Gmail · Blinkit",
                    "created_at": datetime.utcnow(),
                    "updated_at": datetime.utcnow()
                }
            ],
            "expiry_logs": [],
            "smart_cart": [],
            "gap_suggestions": []
        }
    
    @asynccontextmanager
    async def get_connection(self):
        """Get database connection context manager."""
        if not self._initialized:
            await self.initialize()
            
        if self.use_postgres and self.connection_pool:
            try:
                async with self.connection_pool.acquire() as connection:
                    yield connection
            except Exception as e:
                logger.error(f"Failed to acquire database connection: {e}")
                # Fallback to memory store for this operation
                yield self.memory_store
        else:
            yield self.memory_store
    
    async def execute_query(self, query: str, *args) -> List[Dict[str, Any]]:
        """Execute a PostgreSQL query with proper error handling."""
        async with self.get_connection() as conn:
            if self.use_postgres and hasattr(conn, 'fetch'):
                try:
                    result = await conn.fetch(query, *args)
                    return [dict(row) for row in result]
                except Exception as e:
                    logger.error(f"PostgreSQL query failed: {e}")
                    logger.error(f"Query: {query}")
                    logger.error(f"Args: {args}")
                    return []
            else:
                # Fallback implementation for in-memory storage
                logger.debug(f"Executing query on fallback storage: {query}")
                return self._execute_memory_query(query, args)
    
    async def execute_command(self, command: str, *args) -> Union[bool, str]:
        """Execute a PostgreSQL command (INSERT, UPDATE, DELETE) and return success status or ID."""
        async with self.get_connection() as conn:
            if self.use_postgres and hasattr(conn, 'execute'):
                try:
                    result = await conn.execute(command, *args)
                    return True
                except Exception as e:
                    logger.error(f"PostgreSQL command failed: {e}")
                    logger.error(f"Command: {command}")
                    logger.error(f"Args: {args}")
                    return False
            else:
                # Fallback implementation for in-memory storage
                logger.debug(f"Executing command on fallback storage: {command}")
                return self._execute_memory_command(command, args)
    
    async def fetch_one(self, query: str, *args) -> Optional[Dict[str, Any]]:
        """Fetch a single row from PostgreSQL."""
        async with self.get_connection() as conn:
            if self.use_postgres and hasattr(conn, 'fetchrow'):
                try:
                    result = await conn.fetchrow(query, *args)
                    return dict(result) if result else None
                except Exception as e:
                    logger.error(f"PostgreSQL fetchrow failed: {e}")
                    return None
            else:
                # Fallback implementation
                results = self._execute_memory_query(query, args)
                return results[0] if results else None
    
    def _execute_memory_query(self, query: str, args: tuple) -> List[Dict[str, Any]]:
        """Execute query on in-memory storage (simplified implementation)."""
        # This is a simplified implementation for development fallback
        # In a real scenario, you might want to implement a more sophisticated query parser
        
        query_lower = query.lower().strip()
        
        if "select * from inventory" in query_lower:
            return list(self.memory_store["inventory"])
        elif "select * from expiry_logs" in query_lower:
            return list(self.memory_store["expiry_logs"])
        elif "select * from smart_cart" in query_lower:
            return list(self.memory_store["smart_cart"])
        elif "select * from gap_suggestions" in query_lower:
            return list(self.memory_store["gap_suggestions"])
        
        return []
    
    def _execute_memory_command(self, command: str, args: tuple) -> Union[bool, str]:
        """Execute command on in-memory storage (simplified implementation)."""
        command_lower = command.lower().strip()
        
        if command_lower.startswith("insert into inventory"):
            # Generate a new ID and add to memory store
            new_id = str(uuid.uuid4())
            # This is a simplified implementation - in reality you'd parse the INSERT statement
            return new_id
        
        return True
    
    async def health_check(self) -> Dict[str, Any]:
        """Check database health and return status information."""
        if not self._initialized:
            await self.initialize()
        
        status = {
            "database_type": "postgresql" if self.use_postgres else "in_memory",
            "connected": False,
            "pool_size": 0,
            "error": None
        }
        
        if self.use_postgres and self.connection_pool:
            try:
                async with self.connection_pool.acquire() as conn:
                    await conn.execute("SELECT 1")
                    status["connected"] = True
                    status["pool_size"] = self.connection_pool.get_size()
            except Exception as e:
                status["error"] = str(e)
        else:
            status["connected"] = True  # In-memory is always "connected"
        
        return status
    
    async def close(self):
        """Close database connections."""
        if self.connection_pool:
            await self.connection_pool.close()
            logger.info("PostgreSQL connection pool closed")
        self._initialized = False

# Global database manager instance
db_manager = DatabaseManager()