from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..dependencies import get_db
from ..schemas.anime import AnimeCreate, AnimeRead

router = APIRouter(prefix="/anime", tags=["anime"])


@router.get("/", response_model=list[AnimeRead])
async def list_anime(db: AsyncSession = Depends(get_db)) -> list[AnimeRead]:
    # TODO: Replace with database-backed pagination.
    return []


@router.post("/", response_model=AnimeRead, status_code=201)
async def create_anime(payload: AnimeCreate, db: AsyncSession = Depends(get_db)) -> AnimeRead:
    # TODO: Persist anime to database.
    return AnimeRead(
        id=0,
        title=payload.title,
        slug=payload.slug,
        synopsis=payload.synopsis,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )


@router.get("/{anime_id}", response_model=AnimeRead)
async def get_anime(anime_id: int, db: AsyncSession = Depends(get_db)) -> AnimeRead:
    # TODO: Fetch anime by id.
    now = datetime.now()
    return AnimeRead(
        id=anime_id,
        title="placeholder",
        slug=f"anime-{anime_id}",
        synopsis=None,
        created_at=now,
        updated_at=now,
    )

