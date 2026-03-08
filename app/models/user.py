from datetime import datetime, timezone

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class User(Base):
    """
    User model — maps to the 'users' table in the database.
    Each row represents one registered user.
    """

    __tablename__ = "users"

    # Primary key — auto-incremented integer (indexed automatically by the database)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # Email must be unique and is required
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)

    # Full name is required
    full_name: Mapped[str] = mapped_column(String, nullable=False)

    # Timestamp when the user was created; defaults to current UTC time
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )
