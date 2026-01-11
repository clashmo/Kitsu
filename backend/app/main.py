import logging
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse

from .config import settings
from .database import engine
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
from .utils.health import check_database_connection

AVATAR_DIR = Path(__file__).resolve().parent.parent / "uploads" / "avatars"
AVATAR_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger("kitsu")


app = FastAPI(title=settings.app_name, debug=settings.debug)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount(
    "/media/avatars",
    StaticFiles(directory=AVATAR_DIR, html=False),
    name="avatars",
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


@app.on_event("startup")
async def on_startup() -> None:
    logger.info("Starting application")
    if settings.debug:
        logger.warning("DEBUG=true — do not use in production")

    try:
        await check_database_connection(engine)
    except Exception:
        logger.exception("Database connection failed during startup")
    else:
        logger.info("Database connection established")


@app.middleware("http")
async def log_unhandled_exceptions(request, call_next):
    try:
        return await call_next(request)
    except Exception:
        logger.exception("Unhandled exception during request processing")
        raise


@app.get("/health", tags=["health"])
async def healthcheck() -> dict[str, str]:
    try:
        await check_database_connection(engine)
    except Exception:
        logger.exception("Healthcheck database probe failed")
        return JSONResponse(status_code=500, content={"status": "error"})

    logger.info("Healthcheck passed")
    return {"status": "ok"}
