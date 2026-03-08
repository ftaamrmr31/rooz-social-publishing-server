# app/schemas/user.py
#
# Pydantic schemas define the shape of data that comes IN (request body)
# and goes OUT (response body) through the API.
# They are separate from the SQLAlchemy models so that you can control
# exactly what data is exposed to the outside world.

from datetime import datetime

from pydantic import BaseModel


class UserCreate(BaseModel):
    """Schema for creating a new user.

    This is the data a client must send when registering a user.
    """

    email: str
    full_name: str


class UserRead(BaseModel):
    """Schema for reading an existing user.

    This is the data returned by the API when a user is fetched.
    It includes server-generated fields like `id` and `created_at`.
    """

    id: int
    email: str
    full_name: str
    created_at: datetime

    class Config:
        # from_attributes=True allows Pydantic to read data from SQLAlchemy
        # model instances (ORM objects) as if they were plain dicts.
        from_attributes = True
