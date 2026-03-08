from fastapi import FastAPI
from app.core.config import settings
from app.api.router import router

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION
)

app.include_router(router)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "service": settings.APP_NAME}
