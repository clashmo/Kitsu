from sqlalchemy.ext.asyncio import AsyncSession

from ..models.favorite import Favorite
from .base import CRUDBase

favorite_crud = CRUDBase[Favorite](Favorite)


async def add_favorite(session: AsyncSession, data: dict) -> Favorite:
    return await favorite_crud.create(session, data)


async def list_favorites(session: AsyncSession, limit: int = 20, offset: int = 0) -> list[Favorite]:
    return await favorite_crud.list(session, limit=limit, offset=offset)

