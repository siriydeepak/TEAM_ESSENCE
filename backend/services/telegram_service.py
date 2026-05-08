"""
Telegram Bot Service — Aether-Link Protocol (hardened).
Key design decisions:
  - secrets.token_hex() for cryptographically-secure code generation
  - 5-minute TTL enforced at generation AND validation time
  - SyncCodeStore uses database for persistent links, in-memory for pending codes
  - Proactive message helper: notify_user(web_user_id, text)
"""
import os
import logging
import secrets
import hashlib
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import httpx
logger = logging.getLogger(__name__)
TELEGRAM_BOT_TOKEN    = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_BOT_USERNAME = os.getenv("TELEGRAM_BOT_USERNAME", "AetherShelfBot")
TELEGRAM_API          = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"
CODE_TTL_MINUTES = 5   # short window — more secure, better UX
# ---------------------------------------------------------------------------
# SyncCodeStore — manages pending handshakes
# ---------------------------------------------------------------------------
class SyncCodeStore:
    """
    Hybrid store for Aether-Link handshakes.
    - Pending codes: In-memory (short-lived, 5 min TTL)
    - Linked accounts: Database (persistent)
    Replace self._pending with Redis for horizontal scaling.
    """
    def __init__(self):
        # { sync_code: {"web_user_id": str, "created_at": datetime, "used": bool} }
        self._pending: Dict[str, Dict[str, Any]] = {}
        # Cache for linked accounts (loaded from DB on demand)
        self._linked_cache: Dict[str, Dict[str, Any]] = {}
    # ── Generation ──────────────────────────────────────────────────────────
    def generate(self, web_user_id: str) -> str:
        """
        Generate a new 6-digit sync code using secrets module.
        Reuses an existing, unexpired, unused code for the same user if one exists.
        """
        # Purge stale codes first
        self._purge_expired()
        # Return existing live code for this user if any
        for code, meta in self._pending.items():
            if (
                meta["web_user_id"] == web_user_id
                and not meta["used"]
                and meta["created_at"] > datetime.utcnow() - timedelta(minutes=CODE_TTL_MINUTES)
            ):
                return code
        # Cryptographically secure 6-digit code (100000–999999)
        # secrets.token_hex(4) gives 8 hex chars → int → mod 900000 + 100000
        raw = int(secrets.token_hex(4), 16)
        code = str(raw % 900_000 + 100_000)
        # Ensure uniqueness (astronomically unlikely collision, but be safe)
        while code in self._pending:
            raw = int(secrets.token_hex(4), 16)
            code = str(raw % 900_000 + 100_000)
        self._pending[code] = {
            "web_user_id": web_user_id,
            "created_at": datetime.utcnow(),
            "used": False,
        }
        logger.info(f"[AetherLink] Generated sync code for {web_user_id}, expires in {CODE_TTL_MINUTES}m")
        return code
    # ── Validation & Pairing ─────────────────────────────────────────────────
    async def pair(self, code: str, telegram_user_id: int, chat_id: int) -> Optional[str]:
        """
        Validate code and pair telegram_user_id with web_user_id.
        Stores link in database for persistence.
        Returns web_user_id on success, None on any failure.
        """
        self._purge_expired()
        meta = self._pending.get(code)
        if not meta:
            logger.warning(f"[AetherLink] Unknown code: {code}")
            return None
        if meta["used"]:
            logger.warning(f"[AetherLink] Code already used: {code}")
            return None
        if meta["created_at"] < datetime.utcnow() - timedelta(minutes=CODE_TTL_MINUTES):
            logger.warning(f"[AetherLink] Expired code: {code}")
            return None
        web_user_id = meta["web_user_id"]
        meta["used"] = True
        
        # Store in database for persistence
        try:
            from ..utils.database import db_manager
            await db_manager.execute_command("""
                INSERT INTO telegram_links (web_user_id, telegram_user_id, chat_id, linked_at)
                VALUES ($1, $2, $3, $4)
                ON CONFLICT (web_user_id) 
                DO UPDATE SET 
                    telegram_user_id = $2, 
                    chat_id = $3, 
                    linked_at = $4,
                    active = TRUE,
                    updated_at = NOW()
            """, web_user_id, telegram_user_id, chat_id, datetime.utcnow())
            
            # Update cache
            self._linked_cache[web_user_id] = {
                "telegram_user_id": telegram_user_id,
                "chat_id": chat_id,
                "linked_at": datetime.utcnow(),
            }
            logger.info(f"[AetherLink] ✅ Paired {web_user_id} ↔ Telegram {telegram_user_id} (persisted to DB)")
        except Exception as exc:
            logger.error(f"[AetherLink] Failed to persist link to database: {exc}")
            # Fallback to cache-only (will be lost on restart)
            self._linked_cache[web_user_id] = {
                "telegram_user_id": telegram_user_id,
                "chat_id": chat_id,
                "linked_at": datetime.utcnow(),
            }
            logger.warning(f"[AetherLink] ⚠️ Link stored in cache only (not persistent)")
        
        return web_user_id
    # ── Queries ──────────────────────────────────────────────────────────────
    async def is_linked(self, web_user_id: str) -> bool:
        """Check if web user has a linked Telegram account."""
        # Check cache first
        if web_user_id in self._linked_cache:
            return True
        
        # Query database
        try:
            from ..utils.database import db_manager
            result = await db_manager.fetch_one(
                "SELECT * FROM telegram_links WHERE web_user_id = $1 AND active = TRUE",
                web_user_id
            )
            if result:
                # Update cache
                self._linked_cache[web_user_id] = {
                    "telegram_user_id": result["telegram_user_id"],
                    "chat_id": result["chat_id"],
                    "linked_at": result["linked_at"],
                }
                return True
        except Exception as exc:
            logger.error(f"[AetherLink] Database query failed: {exc}")
        
        return False
    
    async def get_chat_id(self, web_user_id: str) -> Optional[int]:
        """Get Telegram chat_id for a web user."""
        # Check cache first
        info = self._linked_cache.get(web_user_id)
        if info:
            return info["chat_id"]
        
        # Query database
        try:
            from ..utils.database import db_manager
            result = await db_manager.fetch_one(
                "SELECT chat_id FROM telegram_links WHERE web_user_id = $1 AND active = TRUE",
                web_user_id
            )
            if result:
                return result["chat_id"]
        except Exception as exc:
            logger.error(f"[AetherLink] Database query failed: {exc}")
        
        return None
    
    async def get_telegram_id(self, web_user_id: str) -> Optional[int]:
        """Get Telegram user_id for a web user."""
        # Check cache first
        info = self._linked_cache.get(web_user_id)
        if info:
            return info["telegram_user_id"]
        
        # Query database
        try:
            from ..utils.database import db_manager
            result = await db_manager.fetch_one(
                "SELECT telegram_user_id FROM telegram_links WHERE web_user_id = $1 AND active = TRUE",
                web_user_id
            )
            if result:
                return result["telegram_user_id"]
        except Exception as exc:
            logger.error(f"[AetherLink] Database query failed: {exc}")
        
        return None
    
    async def get_linked_user(self, telegram_user_id: int) -> Optional[str]:
        """Get web_user_id for a Telegram user."""
        # Check cache first
        for uid, info in self._linked_cache.items():
            if info["telegram_user_id"] == telegram_user_id:
                return uid
        
        # Query database
        try:
            from ..utils.database import db_manager
            result = await db_manager.fetch_one(
                "SELECT web_user_id FROM telegram_links WHERE telegram_user_id = $1 AND active = TRUE",
                telegram_user_id
            )
            if result:
                return result["web_user_id"]
        except Exception as exc:
            logger.error(f"[AetherLink] Database query failed: {exc}")
        
        return None
    def ttl_seconds(self, code: str) -> int:
        """Remaining TTL in seconds for a given code."""
        meta = self._pending.get(code)
        if not meta:
            return 0
        elapsed = (datetime.utcnow() - meta["created_at"]).total_seconds()
        return max(0, int(CODE_TTL_MINUTES * 60 - elapsed))
    # ── Housekeeping ─────────────────────────────────────────────────────────
    def _purge_expired(self):
        cutoff = datetime.utcnow() - timedelta(minutes=CODE_TTL_MINUTES)
        expired = [c for c, m in self._pending.items() if m["created_at"] < cutoff]
        for c in expired:
            del self._pending[c]
        if expired:
            logger.debug(f"[AetherLink] Purged {len(expired)} expired code(s)")
# Global singleton
_store = SyncCodeStore()
# ---------------------------------------------------------------------------
# Public API (used by routes and services)
# ---------------------------------------------------------------------------
def generate_sync_code(web_user_id: str) -> str:
    return _store.generate(web_user_id)
async def pair_code(code: str, telegram_user_id: int, chat_id: int) -> Optional[str]:
    return await _store.pair(code, telegram_user_id, chat_id)
async def is_linked(web_user_id: str) -> bool:
    return await _store.is_linked(web_user_id)
async def get_chat_id(web_user_id: str) -> Optional[int]:
    return await _store.get_chat_id(web_user_id)
async def get_telegram_id(web_user_id: str) -> Optional[int]:
    return await _store.get_telegram_id(web_user_id)
def get_code_ttl(code: str) -> int:
    return _store.ttl_seconds(code)
# ---------------------------------------------------------------------------
# Public compatibility aliases
# pending_links mirrors _store._pending so external code can read it directly.
# Format: { "654321": { "web_user_id": str, "created_at": datetime, "used": bool } }
# ---------------------------------------------------------------------------
@property
def pending_links() -> Dict[str, Any]:
    """Read-only view of pending sync codes (for debug / compatibility)."""
    return _store._pending
# Alias used by the user's example code style
async def process_telegram_update(data: Dict[str, Any]) -> None:
    """Entry point for Telegram webhook updates. Alias for handle_webhook_update."""
    await handle_webhook_update(data)
# Alias to match send_telegram_msg naming used in docs/examples
async def send_telegram_msg(chat_id: int, text: str) -> bool:
    """Alias for send_message — used in user-facing examples."""
    return await send_message(chat_id, text)
# ---------------------------------------------------------------------------
# Telegram API helpers
# ---------------------------------------------------------------------------
async def send_message(chat_id: int, text: str, parse_mode: str = "HTML") -> bool:
    if not TELEGRAM_BOT_TOKEN:
        logger.warning("[Telegram] BOT_TOKEN not set — skipping send")
        return False
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.post(
                f"{TELEGRAM_API}/sendMessage",
                json={"chat_id": chat_id, "text": text, "parse_mode": parse_mode},
            )
            r.raise_for_status()
            return True
    except Exception as exc:
        logger.error(f"[Telegram] send_message failed: {exc}")
        return False
async def notify_user(web_user_id: str, text: str) -> bool:
    """Send a message to the Telegram account linked to this web user."""
    chat_id = await get_chat_id(web_user_id)
    if chat_id is None:
        logger.debug(f"[Telegram] {web_user_id} has no linked account")
        return False
    return await send_message(chat_id, text)
# ---------------------------------------------------------------------------
# Webhook handler
# ---------------------------------------------------------------------------
async def handle_webhook_update(update: Dict[str, Any]) -> None:
    """Process a single Telegram update payload from the webhook."""
    message = update.get("message") or update.get("edited_message")
    if not message:
        return
    chat_id: int        = message["chat"]["id"]
    tg_user_id: int     = message["from"]["id"]
    first_name: str     = message["from"].get("first_name", "there")
    text: str           = (message.get("text") or "").strip()
    # ── /start [optional_code] ───────────────────────────────────────────────
    if text.lower().startswith("/start"):
        parts = text.split(maxsplit=1)
        inline_code = parts[1].strip() if len(parts) > 1 else None
        if inline_code and inline_code.isdigit() and len(inline_code) == 6:
            await _handle_code(inline_code, tg_user_id, chat_id, first_name)
        else:
            await send_message(
                chat_id,
                f"👋 <b>Welcome to AetherShelf, {first_name}!</b>\n\n"
                "Please enter your <b>Kitchen Sync Code</b> from the dashboard to link your inventory.\n\n"
                f"💡 Open the dashboard → <i>Link Your Kitchen</i> section → copy the 6-digit code.\n"
                f"⏱ Codes expire in <b>{CODE_TTL_MINUTES} minutes</b> for security.",
            )
        return
    # ── Raw 6-digit code ─────────────────────────────────────────────────────
    if text.isdigit() and len(text) == 6:
        await _handle_code(text, tg_user_id, chat_id, first_name)
        return
    # ── /status ──────────────────────────────────────────────────────────────
    if text.lower() == "/status":
        linked_user = await _store.get_linked_user(tg_user_id)
        if linked_user:
            await send_message(
                chat_id,
                f"🟢 <b>AetherShelf Status</b>\n\n"
                f"Account: <code>{linked_user}</code>\n"
                f"Kitchen: <b>Linked ✓</b>\n\n"
                f"Use the dashboard to manage your inventory.",
            )
        else:
            await send_message(
                chat_id,
                "⚠️ Your Telegram is not linked yet.\n"
                "Please enter your Kitchen Sync Code from the dashboard.",
            )
        return
    # ── Fallback ─────────────────────────────────────────────────────────────
    await send_message(
        chat_id,
        "🤖 Commands:\n"
        "  /start — Link your kitchen\n"
        "  /status — Connection status\n\n"
        "Or just type your 6-digit Sync Code directly.",
    )
async def _handle_code(code: str, tg_user_id: int, chat_id: int, first_name: str) -> None:
    web_user_id = await pair_code(code, tg_user_id, chat_id)
    if web_user_id:
        await send_message(
            chat_id,
            "✅ <b>Kitchen Linked Successfully!</b>\n\n"
            f"Welcome, <b>{first_name}</b>! Your AetherShelf digital twin is now connected.\n\n"
            "You'll receive real-time alerts for:\n"
            "  🥛 Expiring items\n"
            "  📦 Inventory additions via receipt\n"
            "  🛒 Smart cart suggestions\n\n"
            "<i>Head back to your dashboard — it should update automatically.</i>",
        )
    else:
        await send_message(
            chat_id,
            "❌ <b>Invalid or expired sync code.</b>\n\n"
            f"Codes expire after <b>{CODE_TTL_MINUTES} minutes</b>.\n"
            "Please go back to the dashboard and generate a fresh code.",
        )
