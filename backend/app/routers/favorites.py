from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..dependencies import get_db

router = APIRouter(prefix="/favorites", tags=["favorites"])


@router.get("/")
async def list_favorites(db: AsyncSession = Depends(get_db)) -> list[dict]:
    # TODO: Replace with favorites retrieval.
    return []


@router.post("/", status_code=201)
async def add_favorite(db: AsyncSession = Depends(get_db)) -> dict:
    # TODO: Persist favorite to database.
    return {"message": "favorite added"}

