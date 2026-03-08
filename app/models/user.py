from datetime import datetime, timezone

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class User(Base):
    """User model representing a registered user in the database."""

    __tablename__ = "users"

    # Primary key - auto-incremented unique identifier for each user
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Email address - must be unique and cannot be empty
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    # Full name of the user - cannot be empty
    full_name: Mapped[str] = mapped_column(String, nullable=False)

    # Timestamp when the user was created - defaults to the current UTC time
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
