from datetime import datetime
from pydantic import BaseModel, ConfigDict


class PublishJobCreate(BaseModel):
    platform: str
    content: str


class PublishJobRead(BaseModel):
    id: int
    platform: str
    content: str
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
