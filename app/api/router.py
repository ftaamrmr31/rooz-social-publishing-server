from fastapi import APIRouter
from app.core.config import settings

router = APIRouter(prefix="/api", tags=["api"])

@router.get("/")
async def root():
    """Welcome endpoint"""
    return {"message": "Welcome to Rooz Social Publishing Server API"}

@router.get("/version")
async def version():
    """Get API version"""
    return {"version": settings.APP_VERSION}

@router.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "ok", "service": settings.APP_NAME}