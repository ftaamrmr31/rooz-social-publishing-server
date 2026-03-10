from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from app.db.base import Base


class PublishJob(Base):
    __tablename__ = "publish_jobs"

    id = Column(Integer, primary_key=True, index=True)
    platform = Column(String, index=True, nullable=False)
    content = Column(String, nullable=False)
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
