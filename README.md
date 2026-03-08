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
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py           # Configuration settings
│   ├── db/
│   │   ├── __init__.py
│   │   └── base.py             # Database base classes and configuration (placeholder)
│   ├── models/
│   │   └── __init__.py
│   ├── schemas/
│   │   └── __init__.py
│   └── services/
│       └── __init__.py
├── requirements.txt            # Python dependencies
├── .env.example               # Example environment variables
├── Dockerfile                 # Docker image definition
├── docker-compose.yml         # Docker Compose configuration
├── .gitignore                # Git ignore rules
└── README.md                 # This file
```

## Project Architecture

This project follows a layered architecture pattern to keep code organized and easy to extend.

| Folder | Purpose |
|---|---|
| `app/db/` | Database configuration and base classes. Will contain the SQLAlchemy engine, session factory, and declarative base when a database is added. |
| `app/models/` | Database models (ORM). Each file in this folder will define a SQLAlchemy model that maps to a database table. |
| `app/schemas/` | Pydantic request/response schemas. Used to validate incoming data and shape outgoing responses, keeping the API contract explicit. |
| `app/services/` | Business logic layer. Keeps database queries and application rules out of the route handlers, making the code easier to test and reuse. |
| `app/api/` | API routes and endpoints. FastAPI routers live here; they call service functions and return schema-validated responses. |
| `app/core/` | Application settings and configuration. Environment variables and global constants are loaded here via Pydantic `Settings`. |

## API Documentation

Interactive API documentation is available at:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

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