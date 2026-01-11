from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..dependencies import get_db
from ..schemas.release import ReleaseCreate, ReleaseRead

router = APIRouter(prefix="/releases", tags=["releases"])


@router.get("/", response_model=list[ReleaseRead])
async def list_releases(db: AsyncSession = Depends(get_db)) -> list[ReleaseRead]:
    # TODO: Retrieve releases from database.
    return []


@router.post("/", response_model=ReleaseRead, status_code=201)
async def create_release(payload: ReleaseCreate, db: AsyncSession = Depends(get_db)) -> ReleaseRead:
    # TODO: Persist release to database.
    return ReleaseRead(id=0, anime_id=payload.anime_id, status=payload.status, released_at=datetime.now())

