import logging
import os
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Awaitable, Callable

from fastapi import FastAPI, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

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

log_level_name = os.getenv("LOG_LEVEL", "INFO").upper()


def _resolve_log_level(value: str) -> int:
    level = logging.getLevelName(value)
    return level if isinstance(level, int) else logging.INFO


log_level = _resolve_log_level(log_level_name)

if not logging.getLogger().handlers:
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
logger = logging.getLogger("kitsu")
logger.setLevel(log_level)


def _health_response(status_text: str, status_code: int) -> JSONResponse:
    return JSONResponse(status_code=status_code, content={"status": status_text})

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting application")
    if settings.debug:
        logger.warning("DEBUG=true — do not use in production")

    try:
        await check_database_connection(engine)
    except SQLAlchemyError:
        logger.exception("Database connection failed during startup")
        # Continue startup so /health can report database status
    else:
        logger.info("Database connection established")

    yield


app = FastAPI(title=settings.app_name, debug=settings.debug, lifespan=lifespan)

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


@app.middleware("http")
async def log_unhandled_exceptions(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    try:
        return await call_next(request)
    except Exception:
        logger.exception("Unhandled exception during request processing")
        raise


@app.get("/health", tags=["health"])
async def healthcheck() -> Response:
    try:
        await check_database_connection(engine)
    except SQLAlchemyError as exc:
        logger.error("Healthcheck database probe failed: %s", exc)
        return _health_response("error", status.HTTP_500_INTERNAL_SERVER_ERROR)

    logger.debug("Healthcheck passed")
    return _health_response("ok", status.HTTP_200_OK)
