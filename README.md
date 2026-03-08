# Rooz Social Publishing Server

A production-style backend API for social publishing built with FastAPI.

## Overview

This is a clean, beginner-friendly starter project for a FastAPI backend server. It follows production best practices while remaining simple and easy to understand.

## Requirements

- Docker
- Docker Compose
- Python 3.12 (for local development)

## Quick Start with Docker

### 1. Clone the repository
```bash
git clone https://github.com/ftaamrmr31/rooz-social-publishing-server.git
cd rooz-social-publishing-server
```

### 2. Set up environment variables
```bash
cp .env.example .env
```

### 3. Run with Docker Compose
```bash
docker-compose up
```

The API will be available at `http://localhost:8000`

## Available Endpoints

### Health Check
```bash
GET http://localhost:8000/health
```
Response:
```json
{
  "status": "ok",
  "service": "rooz-social-publishing-server"
}
```

### API Root
```bash
GET http://localhost:8000/api/
```
Response:
```json
{
  "message": "Welcome to Rooz Social Publishing Server API"
}
```

### API Version
```bash
GET http://localhost:8000/api/version
```
Response:
```json
{
  "version": "0.1.0"
}
```

## Local Development (without Docker)

### 1. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Copy environment file
```bash
cp .env.example .env
```

### 4. Run the server
```bash
python app/main.py
```

Or use uvicorn directly:
```bash
uvicorn app.main:app --reload
```

## Project Structure

```
rooz-social-publishing-server/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app initialization
│   ├── api/
│   │   ├── __init__.py
│   │   └── router.py           # API routes
│   └── core/
│       ├── __init__.py
│       └── config.py           # Configuration settings
├── requirements.txt            # Python dependencies
├── .env.example               # Example environment variables
├── Dockerfile                 # Docker image definition
├── docker-compose.yml         # Docker Compose configuration
├── .gitignore                # Git ignore rules
└── README.md                 # This file
```

## API Documentation

Interactive API documentation is available at:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Database Setup

This project uses **SQLAlchemy** as the ORM (Object Relational Mapper) and **SQLite** as the database for development.

### ORM

[SQLAlchemy](https://www.sqlalchemy.org/) maps Python classes to database tables, so you can work with database records as regular Python objects instead of writing raw SQL.

### Database

SQLite is a lightweight, file-based database that requires no separate server process. The database file (`test.db`) is created automatically in the project root when tables are first created. It is ideal for development and testing.

### How to Create Tables (future step)

Once models are defined, you can create the tables by running:

```python
from app.db.base import Base
from app.db.session import engine
import app.models  # ensure all models are registered

Base.metadata.create_all(bind=engine)
```

### Location of Models and Schemas

| Component | Path | Description |
|-----------|------|-------------|
| Declarative base | `app/db/base.py` | Base class that all ORM models inherit from |
| Engine & session | `app/db/session.py` | Database connection and `get_db` dependency |
| User model | `app/models/user.py` | SQLAlchemy ORM model for the `users` table |
| User schemas | `app/schemas/user.py` | Pydantic schemas for input (`UserCreate`) and output (`UserRead`) |

## Next Steps

This is a starter project with the essentials configured. Future additions could include:

- Database integration (PostgreSQL, SQLAlchemy)
- Authentication (JWT, OAuth2)
- Caching (Redis)
- Logging and monitoring
- API versioning
- Rate limiting
- Background tasks (Celery)

## Contributing

Please follow PEP 8 style guide and maintain the current code structure.

## License

MIT License