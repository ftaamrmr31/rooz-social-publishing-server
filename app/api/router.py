from fastapi import APIRouter

from app.api.users import users_router

router = APIRouter(prefix="/api", tags=["api"])


@router.get("/")
async def root():
    return {"message": "Welcome to Rooz Social Publishing Server API"}


@router.get("/version")
async def version():
    return {"version": "0.1.0"}


router.include_router(users_router, prefix="/users", tags=["users"])
