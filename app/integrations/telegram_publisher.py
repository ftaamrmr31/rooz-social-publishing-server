import httpx
from app.core.config import settings


def send_telegram_message(content: str) -> dict:
    """Send a message to Telegram using the Bot API."""
    if not settings.TELEGRAM_BOT_TOKEN:
        raise ValueError("TELEGRAM_BOT_TOKEN is not configured")
    if not settings.TELEGRAM_CHAT_ID:
        raise ValueError("TELEGRAM_CHAT_ID is not configured")

    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": settings.TELEGRAM_CHAT_ID,
        "text": content,
    }

    response = httpx.post(url, json=payload)
    response.raise_for_status()
    return response.json()
