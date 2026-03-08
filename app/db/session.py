from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# SQLite database URL (file-based)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# Create database engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},  # SQLite specific
)

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db():
    """Dependency for getting database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
