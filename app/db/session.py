# app/db/session.py
#
# This module sets up the SQLAlchemy database engine and session factory.
# It is the single place where the database connection is configured.

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# DATABASE_URL comes from the app settings (see app/core/config.py).
# By default it points to a local SQLite file: test.db in the project root.
# SQLite is great for development because it requires no separate server.
# To use a different database (e.g. PostgreSQL in production), set the
# DATABASE_URL environment variable, e.g.:
#   DATABASE_URL=postgresql://user:pass@localhost/dbname
DATABASE_URL = settings.DATABASE_URL

# The engine is the low-level object that manages the actual database connection.
# connect_args={"check_same_thread": False} is required for SQLite when using
# FastAPI, because FastAPI may access the database from multiple threads.
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

# SessionLocal is a factory for creating new database sessions.
# Each request should open its own session, use it, and then close it.
# autocommit=False  → changes are not saved until you explicitly call session.commit()
# autoflush=False   → objects are not automatically flushed to the DB before every query
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
