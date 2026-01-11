# Frontend (Next.js)

## Purpose

User-facing web app for browsing anime and playback via an HLS proxy. It interacts with the FastAPI backend for data (anime lists/search, auth-dependent features in progress).

## Tech Stack

- Next.js 15 (app router), React 18
- Tailwind CSS, shadcn/ui
- React Query, Axios, zustand
- next-runtime-env for runtime env injection
- ArtPlayer + HLS.js

## Environment Variables (required)

- `NEXT_PUBLIC_API_URL` – Base URL of the FastAPI backend (e.g., `http://localhost:8000`)
- `NEXT_PUBLIC_PROXY_URL` – Base URL of the HLS/m3u8 proxy (e.g., `http://localhost:4040`)

Set these in `.env.local` (local) or Render env vars (production). The app will fail to fetch data if `NEXT_PUBLIC_API_URL` is unset.

## Running Locally

```bash
npm install
NEXT_PUBLIC_API_URL=http://localhost:8000 \
NEXT_PUBLIC_PROXY_URL=http://localhost:4040 \
npm run dev
```

The frontend requires the FastAPI backend to be running and reachable at `NEXT_PUBLIC_API_URL`.

## Production (Render)

1. Build using the provided `Dockerfile` (standalone Next.js output).  
2. Configure env vars: `NEXT_PUBLIC_API_URL` (public backend URL) and `NEXT_PUBLIC_PROXY_URL` (public proxy URL).  
3. Deploy the image; expose port 3000.  
4. Ensure the backend is deployed and reachable; frontend will not function without it.

## Backend Dependency

- All API data (anime list, search, auth) is expected from the FastAPI backend.
- Without the backend, pages relying on `/anime` or `/search/anime` will render empty/errored states.

## Hybrid Data Sources

- Some playback/search paths still use HiAnime scraper endpoints exposed via Next API routes. Media streaming also depends on `NEXT_PUBLIC_PROXY_URL`.
- Backend is authoritative for core data; scraper routes are supplemental and may differ in IDs/shape.

## Known Limitations

- Auth UI and API wiring are incomplete; refresh/login flows are not fully exposed in the UI.  
- Anime data uses placeholders for posters/episodes when backend omits fields.  
- Proxy/HLS must be reachable; missing `NEXT_PUBLIC_PROXY_URL` breaks playback.  
- Error handling is minimal; backend downtime results in empty sections without detailed messaging.
