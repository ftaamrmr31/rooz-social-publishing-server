import secrets
from typing import Optional

from fastapi import Header, HTTPException
from app.core.config import settings


async def verify_api_key(x_api_key: Optional[str] = Header(default=None)):
    """
    API key dependency.

    - If API_SECRET_KEY is empty (development mode), all requests are allowed.
    - If API_SECRET_KEY is set, the request must include a matching X-API-Key header.
    """
    # Development mode: no key configured (or whitespace-only), skip check
    if not settings.API_SECRET_KEY.strip():
        return

    # Production mode: require a valid, matching key.
    # Explicit empty/None check before secrets.compare_digest (which requires
    # both arguments to be non-None strings).  Constant-time comparison via
    # compare_digest prevents timing-based key discovery attacks.
    if not x_api_key or not secrets.compare_digest(x_api_key, settings.API_SECRET_KEY):
        raise HTTPException(status_code=401, detail="Invalid or missing API key")
