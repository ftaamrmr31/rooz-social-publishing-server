# Schemas for PublishJob API

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class PublishJobCreate(BaseModel):
    """Input schema for creating a publish job."""
    platform: str
    content: str


class PublishJobRead(BaseModel):
    """Schema for reading publish job records."""
    id: int
    platform: str
    content: str
    status: str
    created_at: datetime

    # Enable Pydantic v2 ORM/model validation so SQLAlchemy models
    # can be returned directly from endpoints.
    model_config = ConfigDict(from_attributes=True)
