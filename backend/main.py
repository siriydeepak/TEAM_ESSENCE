"""
AetherShelf Backend — FastAPI entry point.

Run from the project root:
  python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
"""

import os
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routes import (
    inventory_router,
    weather_router,
    analytics_router,
    receipts_router,
    smart_cart_router,
    gap_finder_router,
    auth_router,
    automation_router,
    telegram_router,
    virtual_kitchen_router,
)
from backend.utils.database import db_manager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("AetherShelf API starting up…")
    await db_manager.initialize()
    yield
    logger.info("AetherShelf API shutting down…")
    await db_manager.close()


app = FastAPI(
    title="AetherShelf API",
    description="Smart pantry intelligence — Aether-Link Protocol & Virtual Kitchen",
    version="2.1.0",
    lifespan=lifespan,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router,            prefix="/api/auth",            tags=["Auth"])
app.include_router(inventory_router,       prefix="/api/inventory",       tags=["Inventory"])
app.include_router(weather_router,         prefix="/api/weather",         tags=["Weather"])
app.include_router(analytics_router,       prefix="/api/analytics",       tags=["Analytics"])
app.include_router(receipts_router,        prefix="/api/receipts",        tags=["Receipts"])
app.include_router(smart_cart_router,      prefix="/api/smart-cart",      tags=["SmartCart"])
app.include_router(gap_finder_router,      prefix="/api/gap-finder",      tags=["GapFinder"])
app.include_router(automation_router,      prefix="/api/automation",      tags=["Automation"])
app.include_router(telegram_router,        prefix="/api/telegram",        tags=["Telegram"])
app.include_router(virtual_kitchen_router, prefix="/api/kitchen",         tags=["VirtualKitchen"])


@app.get("/api/health", tags=["System"])
async def health():
    db_status = await db_manager.health_check()
    return {
        "status": "ok",
        "version": "2.1.0",
        "database": db_status,
        "telegram_bot": bool(os.getenv("TELEGRAM_BOT_TOKEN")),
        "gemini_ai": bool(os.getenv("GEMINI_API_KEY")),
    }


@app.get("/api", tags=["System"])
async def root():
    return {"message": "AetherShelf API v2.1 — Aether-Link Protocol active"}
