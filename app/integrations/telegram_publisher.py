# Telegram integration — sends a text message via the Telegram Bot API.

import requests

from app.core.config import settings


def send_telegram_message(text: str) -> dict:
    """
    Send a text message to a Telegram chat using the configured bot.

    Args:
        text: The message text to send.

    Returns:
        The JSON response from the Telegram API as a Python dict.

    Raises:
        ValueError: If TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID is not set.
        requests.HTTPError: If the Telegram API returns an error status code.
    """
    # Make sure the required settings are present before making any HTTP call.
    if not settings.TELEGRAM_BOT_TOKEN:
        raise ValueError(
            "TELEGRAM_BOT_TOKEN is not set. "
            "Add it to your .env file before using the Telegram integration."
        )

    if not settings.TELEGRAM_CHAT_ID:
        raise ValueError(
            "TELEGRAM_CHAT_ID is not set. "
            "Add it to your .env file before using the Telegram integration."
        )

    # Build the Telegram Bot API URL for the sendMessage method.
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"

    # Payload expected by the Telegram API.
    payload = {
        "chat_id": settings.TELEGRAM_CHAT_ID,
        "text": text,
    }

    # Send the POST request and raise an exception for 4xx/5xx responses.
    response = requests.post(url, json=payload, timeout=10)
    response.raise_for_status()

    # Return the parsed JSON so the caller can inspect the result.
    return response.json()
