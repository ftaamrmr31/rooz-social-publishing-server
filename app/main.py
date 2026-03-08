from app.db.base import Base
from app.db.session import engine
from fastapi import FastAPI
from app.api.router import router
from app.core.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    description="Backend API for Rooz Social Publishing Server",
    version=settings.APP_VERSION,
)

Base.metadata.create_all(bind=engine)

app.include_router(router)


@app.get("/health", tags=["health"])
async def health_check():
    return {"status": "ok", "service": settings.APP_NAME}
