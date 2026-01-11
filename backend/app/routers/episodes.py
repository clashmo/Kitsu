from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..dependencies import get_db
from ..schemas.episode import EpisodeCreate, EpisodeRead

router = APIRouter(prefix="/episodes", tags=["episodes"])


@router.get("/", response_model=list[EpisodeRead])
async def list_episodes(db: AsyncSession = Depends(get_db)) -> list[EpisodeRead]:
    # TODO: Retrieve episodes from database.
    return []


@router.post("/", response_model=EpisodeRead, status_code=201)
async def create_episode(payload: EpisodeCreate, db: AsyncSession = Depends(get_db)) -> EpisodeRead:
    # TODO: Persist episode to database.
    return EpisodeRead(
        id=0,
        anime_id=payload.anime_id,
        number=payload.number,
        title=payload.title,
        synopsis=payload.synopsis,
        aired_at=payload.aired_at or datetime.now(),
    )

