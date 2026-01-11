from sqlalchemy.ext.asyncio import AsyncSession

from ..models.anime import Anime
from .base import CRUDBase

anime_crud = CRUDBase[Anime](Anime)


async def create_anime(session: AsyncSession, data: dict) -> Anime:
    return await anime_crud.create(session, data)


async def list_anime(session: AsyncSession, limit: int = 20, offset: int = 0) -> list[Anime]:
    return await anime_crud.list(session, limit=limit, offset=offset)

