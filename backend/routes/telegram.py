"""
Telegram integration API routes — Aether-Link Protocol.

Endpoints:
  POST /api/telegram/webhook        — Telegram webhook receiver
  POST /api/telegram/generate-code  — Generate a Kitchen Sync Code for the logged-in user
  GET  /api/telegram/status         — Check whether the current user has a linked Telegram account
  POST /api/telegram/notify         — Send a one-off message to the linked Telegram account
"""

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from typing import Optional
import os

from ..services.telegram_service import (
    generate_sync_code,
    process_telegram_update,   # canonical entry-point
    handle_webhook_update,     # kept for backward compat
    notify_user,
    is_linked,
    get_telegram_id,
    get_chat_id,
    get_code_ttl,
)

router = APIRouter()


# ---------------------------------------------------------------------------
# Pydantic models
# ---------------------------------------------------------------------------

class SyncCodeRequest(BaseModel):
    web_user_id: str   # e.g. email or UUID from your auth system


class NotifyRequest(BaseModel):
    web_user_id: str
    message: str


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.post("/webhook")
async def telegram_webhook(request: Request):
    """
    Aether-Link entry point — Telegram sends every user message here.
    Handles /start, raw 6-digit codes, and /status commands.
    Always returns 200 so Telegram never retries on our errors.
    """
    try:
        data = await request.json()
        await process_telegram_update(data)   # ← canonical handler
        return {"status": "ok"}
    except Exception as exc:
        # Log but never raise — Telegram retries on non-200
        return {"status": "error", "detail": str(exc)}


@router.post("/generate-code")
async def generate_code(body: SyncCodeRequest):
    """
    Generate (or retrieve) a 6-digit Kitchen Sync Code.
    Valid for 5 minutes. Reuses existing live code for the same user.
    """
    if not body.web_user_id:
        raise HTTPException(status_code=400, detail="web_user_id is required")

    code           = generate_sync_code(body.web_user_id)
    already_linked = is_linked(body.web_user_id)
    ttl            = get_code_ttl(code)
    bot_username   = os.getenv("TELEGRAM_BOT_USERNAME", "AetherShelfBot")

    return {
        "success": True,
        "sync_code": code,
        "already_linked": already_linked,
        "telegram_id": get_telegram_id(body.web_user_id),
        "ttl_seconds": ttl,
        "message": (
            "Kitchen already linked to Telegram" if already_linked
            else f"Your Kitchen Sync Code is {code}. Valid for {ttl} seconds."
        ),
        "bot_url": f"https://t.me/{bot_username}?start={code}",
    }


@router.get("/status")
async def get_link_status(web_user_id: str):
    """Check whether a web account has a linked Telegram account."""
    linked = is_linked(web_user_id)
    return {
        "success": True,
        "linked": linked,
        "telegram_id": get_telegram_id(web_user_id) if linked else None,
    }


@router.post("/notify")
async def send_notification(body: NotifyRequest):
    """Send a Telegram message to the user linked to web_user_id."""
    if not body.web_user_id or not body.message:
        raise HTTPException(status_code=400, detail="web_user_id and message are required")

    sent = await notify_user(body.web_user_id, body.message)
    return {
        "success": sent,
        "message": "Notification sent" if sent else "User not linked or send failed",
    }


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def _bot_username() -> str:
    import os
    return os.getenv("TELEGRAM_BOT_USERNAME", "AetherShelfBot")
