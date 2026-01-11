# Kitsu Backend

FastAPI service providing the authoritative API for the Kitsu frontend. Uses PostgreSQL via async SQLAlchemy 2.x and Alembic migrations. Legacy PocketBase is deprecated.

## Tech Stack

- FastAPI
- SQLAlchemy 2 (async) + asyncpg
- Alembic
- PyJWT, passlib (bcrypt)
- Uvicorn

## Environment Variables (complete)

Copy `.env.example` to `.env` and set the following:

- `SECRET_KEY` (required) – JWT signing key. Backend refuses to start if missing.
- `DATABASE_URL` – e.g., `postgresql+asyncpg://USER:PASS@HOST:PORT/DB`.
  - Docker Compose: set `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`; the compose file constructs `DATABASE_URL`.
  - Local runs: set `DATABASE_URL` directly.
- `ACCESS_TOKEN_EXPIRE_MINUTES` – default 30
- `REFRESH_TOKEN_EXPIRE_DAYS` – default 14
- `ALGORITHM` – default `HS256`
- `ALLOWED_ORIGINS` – comma-separated list for CORS (must not be `*` when sending credentials)
- `DEBUG` – `true`/`false` (enables SQL echo)
- `APP_NAME` (optional)

In `backend/docker-compose.yml`, the `DATABASE_URL` environment value uses shell-style interpolation of `DB_*` variables (see the `environment` block for the backend service). Provide either a full `DATABASE_URL` or the individual `DB_*` values before starting the stack.

## Running Locally (without Docker)

```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -e .
export SECRET_KEY="change-me"
export DATABASE_URL="postgresql+asyncpg://kitsu:kitsu@localhost:5432/kitsu"
uvicorn app.main:app --reload
```

## Running with Docker

```bash
docker compose up --build
docker compose run --rm backend alembic upgrade head
```

- File: `backend/docker-compose.yml` (includes Postgres)
- API: `http://localhost:8000` (Swagger: `/docs`)

## Alembic Migrations

- Apply: `alembic upgrade head`
- Create (if needed): `alembic revision -m "message"`
- Run migrations after schema changes and before serving production traffic.

## Uploads and Avatars

- Stored under `backend/uploads/avatars` on the backend filesystem.
- No CDN or remote storage; files are **ephemeral** in containerized/cloud deploys unless a persistent volume is mounted. Mount this path in production to avoid avatar loss.

## Known Limitations (current state)

- User CRUD endpoints are placeholders beyond auth-protected avatar upload.  
- CORS is permissive by default; configure `ALLOWED_ORIGINS` for real deployments.  
- Healthcheck does not verify DB connectivity.  
- Single refresh token per user (multi-device sessions not supported).  
- No rate limiting or brute-force protection on auth endpoints.  
- Uploads are local-only and not backed by persistent storage.
