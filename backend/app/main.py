from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .routers import (
    anime,
    auth,
    collections,
    episodes,
    favorites,
    releases,
    search,
    users,
    views,
)

app = FastAPI(title=settings.app_name, debug=settings.debug)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

routers = [
    auth.router,
    users.router,
    anime.router,
    releases.router,
    episodes.router,
    collections.router,
    favorites.router,
    views.router,
]

for router in routers:
    app.include_router(router)

app.include_router(search.router, tags=["Search"])


@app.get("/health", tags=["health"])
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}
