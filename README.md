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

## API Key Protection

Protected endpoints require an `X-API-Key` header when `API_SECRET_KEY` is set in your `.env` file.

| Mode | `API_SECRET_KEY` value | Behaviour |
|------|------------------------|-----------|
| Development | *(empty or whitespace-only)* | All requests are allowed — no key needed |
| Production | `your-secret-key` | Requests without a valid key are rejected with **HTTP 401** |

### Protected endpoints
- `POST /api/publish`
- `POST /api/publish/telegram/send-now`

### Unprotected endpoints (always public)
- `GET /api/publish`
- `GET /health`
- `GET /api/`
- `GET /api/version`

### Examples

**Without API key — fails when `API_SECRET_KEY` is set:**
```bash
curl -k -X POST https://api.auto4store.cloud/api/publish \
  -H "Content-Type: application/json" \
  -d '{"platform":"telegram","content":"Test message"}'
# → HTTP 401 {"detail":"Invalid or missing API key"}
```

**With API key — succeeds:**
```bash
curl -k -X POST https://api.auto4store.cloud/api/publish \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-secret-key" \
  -d '{"platform":"telegram","content":"Test message"}'
```

**Send Telegram message now:**
```bash
curl -k -X POST https://api.auto4store.cloud/api/publish/telegram/send-now \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-secret-key" \
  -d '{"content":"Hello from Rooz!"}'
```

### Setup

1. Copy the example env file and set your key:
   ```bash
   cp .env.example .env
   # Edit .env and set: API_SECRET_KEY=your-secret-key
   ```
2. Restart the server — the key takes effect immediately.

---



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