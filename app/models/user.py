# app/models/user.py
#
# This module defines the User database model using SQLAlchemy ORM.
# A "model" is a Python class that maps directly to a database table.

from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer, String

from app.db.base import Base


class User(Base):
    """Represents a user account stored in the 'users' table.

    Fields:
        id        - Auto-incrementing integer primary key.
        email     - Unique email address used to identify the user.
        full_name - User's display name.
        created_at- Timestamp recorded automatically when the row is created.
    """

    __tablename__ = "users"

    # Primary key — SQLAlchemy generates a unique integer for each new row.
    id = Column(Integer, primary_key=True, index=True)

    # Email must be unique across all users.
    # index=True speeds up lookups by email.
    email = Column(String(255), unique=True, index=True, nullable=False)

    # Full name is optional (nullable=True by default in SQLAlchemy).
    full_name = Column(String(200), nullable=True)

    # created_at is set automatically to the current UTC time on insert.
    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
