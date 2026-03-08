from fastapi import FastAPI
from app.api.router import router

# Initialize FastAPI app
app = FastAPI(
    title="Rooz Social Publishing Server",
    description="A production-style backend API for social publishing",
    version="0.1.0"
)

# Include routers
app.include_router(router)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "service": "rooz-social-publishing-server"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)