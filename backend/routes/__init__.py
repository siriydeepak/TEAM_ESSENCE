# Backend routes module

from .inventory import router as inventory_router
from .weather import router as weather_router
from .analytics import router as analytics_router
from .receipts import router as receipts_router
from .smart_cart import router as smart_cart_router
from .gap_finder import router as gap_finder_router
from .auth import router as auth_router
from .automation import router as automation_router

__all__ = [
    "inventory_router",
    "weather_router", 
    "analytics_router",
    "receipts_router",
    "smart_cart_router",
    "gap_finder_router",
    "auth_router",
    "automation_router"
]