from datetime import datetime

from pydantic import BaseModel, ConfigDict


class UserCreate(BaseModel):
    """
    Schema for creating a new user.
    This is the data the client sends in the request body.
    """

    email: str
    full_name: str


class UserRead(BaseModel):
    """
    Schema for reading/returning user data.
    This is what the API sends back to the client.
    """

    id: int
    email: str
    full_name: str
    created_at: datetime

    # from_attributes=True allows Pydantic to read data from SQLAlchemy model
    # instances (ORM objects) in addition to plain dictionaries.
    model_config = ConfigDict(from_attributes=True)
