# Rooz Social Publishing Server

A production-style backend API for social publishing built with FastAPI.

## Requirements

- Docker and Docker Compose
- Python 3.12 (for local development)

## Run with Docker

```bash
cp .env.example .env
docker-compose up
```

The API will be available at `http://localhost:8000`

## Run Locally (without Docker)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
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
│   │   └── router.py           # API routes (/api/, /api/version)
│   └── core/
│       ├── __init__.py
│       └── config.py           # Configuration settings
├── requirements.txt
├── .env.example
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check |
| GET | `/api/` | API welcome message |
| GET | `/api/version` | API version |

## API Documentation

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`