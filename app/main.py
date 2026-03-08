from fastapi import FastAPI
from app.api.router import router
from app.core.config import settings

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="A production-style backend API for social publishing",
    version=settings.APP_VERSION
)

# Include routers
app.include_router(router)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "service": settings.APP_NAME}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)