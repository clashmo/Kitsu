![logo.png](logo.png)

# Kitsu

An open-source anime streaming web app in pre-production/MVP stabilization. The stack is split between a FastAPI backend (authoritative API) and a Next.js frontend. The legacy PocketBase backend is **deprecated and not used**.

## Architecture (text)

```
[Next.js Frontend] --(REST/JSON over HTTP(S))--> [FastAPI Backend] --(SQLAlchemy)--> [PostgreSQL]
        |
        +--(HiAnime scraper via Next API routes for media sources)

[Static uploads] served from FastAPI /media/avatars (local filesystem; no CDN)
```

## Tech Stack

- Frontend: Next.js 15, React 18, Tailwind, shadcn/ui, React Query, Axios
- Backend: FastAPI, SQLAlchemy 2 (async), Alembic, PostgreSQL
- Misc: next-runtime-env, ArtPlayer/HLS, HiAnime scraper helper

## Repository Structure

- `src/` – Next.js app (frontend)
- `backend/` – FastAPI service (backend)
- `docker-compose.yml` – legacy compose (frontend + proxy only; PocketBase deprecated)
- `backend/docker-compose.yml` – backend + Postgres compose
- `Dockerfile` – frontend image
- `backend/Dockerfile` – backend image
- `docs/` – legacy artifacts

## Running the project (high-level)

### Local (recommended)

1) Backend  
   - Copy `backend/.env.example` to `backend/.env` and set required variables (see `backend/README.md`).  
   - Start Postgres (e.g., `docker compose -f backend/docker-compose.yml up db`).  
   - Run migrations: `docker compose -f backend/docker-compose.yml run --rm backend alembic upgrade head`.  
   - Start API: `uvicorn app.main:app --reload` (or `docker compose up backend`).

2) Frontend  
   - Set `NEXT_PUBLIC_API_URL` to the FastAPI URL and `NEXT_PUBLIC_PROXY_URL` for the m3u8 proxy.  
   - `npm install`  
   - `npm run dev`

The frontend depends on the backend API; it will not function correctly without it.

### Production / Render (overview)

- Build Docker images using the provided Dockerfiles (frontend and backend separately).  
- Provision PostgreSQL and apply Alembic migrations before serving traffic.  
- Mount persistent storage for `backend/uploads/avatars` or accept avatar loss on redeploy.  
- Configure env vars on Render: see backend/frontend READMEs for required keys.  
- Serve frontend with `NEXT_PUBLIC_API_URL` pointing to the backend’s public URL and `NEXT_PUBLIC_PROXY_URL` set to your HLS proxy.

## PocketBase Status

PocketBase is deprecated and not used. The authoritative backend is FastAPI.

## Further documentation

- Backend: [`backend/README.md`](backend/README.md)
- Frontend: [`frontend/README.md`](frontend/README.md)
- Roadmap: [`ROADMAP.md`](ROADMAP.md)
