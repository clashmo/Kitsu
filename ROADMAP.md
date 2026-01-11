# Roadmap

## Phase 1 — MVP (current)
- Solidify auth flow (login/register/refresh/logout in UI + backend)
- Wire frontend to FastAPI for anime list/search/favorites/profile
- Replace PocketBase remnants and align env vars (API/proxy)
- Document and automate migrations for production; configure CORS and secrets
- Persist avatars via mounted storage
- Out of scope for this phase: analytics, multi-device refresh tokens, and CDN

## Phase 2 — Post-MVP Hardening
- Expand backend features: releases/episodes/watch history and views
- Improve error handling and UX for backend outages
- Add logging/metrics, rate limiting, and DB health checks
- Clean up hybrid data sources; align IDs between backend and scraper pathways
- Introduce CI for lint/test/build and migration checks

## Phase 3 — Future
- Multi-session token support and device management
- Media/proxy/CDN strategy and caching
- Advanced recommendations/analytics
- Performance tuning and scaling guidance
