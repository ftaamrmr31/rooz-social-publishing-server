import httpx

from app.core.config import settings


TELEGRAM_API_BASE = "https://api.telegram.org"


def send_telegram_message(content: str) -> dict:
    """Send a message to Telegram using the Bot API."""
    if not settings.TELEGRAM_BOT_TOKEN:
        raise ValueError("TELEGRAM_BOT_TOKEN is not configured")

    if not settings.TELEGRAM_CHAT_ID:
        raise ValueError("TELEGRAM_CHAT_ID is not configured")

    url = f"{TELEGRAM_API_BASE}/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": settings.TELEGRAM_CHAT_ID,
        "text": content,
    }

    try:
        with httpx.Client(timeout=10.0) as client:
            response = client.post(url, json=payload)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as exc:
        raise RuntimeError(
            f"Telegram API returned status {exc.response.status_code}"
        ) from exc
    except httpx.RequestError as exc:
        raise RuntimeError("Failed to connect to Telegram API") from exc
