from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# SQLite database file will be created in the project root
SQLALCHEMY_DATABASE_URL = "sqlite:///./rooz.db"

# Create the SQLAlchemy engine
# check_same_thread=False is required for SQLite when used with FastAPI
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

# SessionLocal is a factory for creating new database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    FastAPI dependency that provides a database session.
    Yields a session and ensures it is closed after the request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
