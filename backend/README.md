# Kitsu Backend

FastAPI-based backend rewrite for the Kitsu anime website, intended to replace the existing backend while the current frontend remains unchanged. This project uses PostgreSQL, SQLAlchemy 2.0 (async), and Alembic for migrations.

## Prerequisites

- Docker and Docker Compose
- Python 3.12 (for running locally without containers)

## Environment

Copy the example environment file and adjust values as needed:

```bash
cp .env.example .env
```

## Running with Docker

Build and start the backend and PostgreSQL services:

```bash
docker compose up --build
```

Apply database migrations once the services are up:

```bash
docker compose run --rm backend alembic upgrade head
```

The API will be available at `http://localhost:8000`. Swagger UI is accessible at `/docs`.

## Local Development (without Docker)

```bash
pip install --upgrade pip
pip install -e .
export DATABASE_URL="postgresql+asyncpg://kitsu:kitsu@localhost:5432/kitsu"
uvicorn app.main:app --reload
```

## Project Structure

- `app/`: FastAPI application code (routers, models, schemas, CRUD, utils).
- `alembic/`: Migration environment and templates.
- `docker-compose.yml`: Orchestrates backend and PostgreSQL services.
- `Dockerfile`: Container image definition for the backend.
