from pydantic import BaseModel
from datetime import datetime


class UserCreate(BaseModel):
    email: str
    full_name: str


class UserRead(BaseModel):
    id: int
    email: str
    full_name: str
    created_at: datetime

    class Config:
        from_attributes = True
