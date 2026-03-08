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

This project uses **SQLAlchemy** (an ORM) with **SQLite** for local development.

### How it works

| File | Purpose |
|------|---------|
| `app/db/base.py` | Defines `Base`, the parent class all models inherit from |
| `app/db/session.py` | Creates the database engine and `SessionLocal` factory |
| `app/models/user.py` | `User` model — maps to the `users` table in the database |
| `app/schemas/user.py` | Pydantic schemas (`UserCreate`, `UserRead`) for request/response validation |

SQLite stores everything in a single file (`test.db`) in the project root, so no
extra database server is needed during development.

### Adding more models

1. Create a new file in `app/models/`, e.g. `app/models/post.py`.
2. Define your model class inheriting from `Base` (see `user.py` for an example).
3. Import the model in `app/models/__init__.py` so SQLAlchemy discovers the table.

## Next Steps

This is a starter project with the essentials configured. Future additions could include:

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