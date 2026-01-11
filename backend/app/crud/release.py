from sqlalchemy.ext.asyncio import AsyncSession

from ..models.release import Release
from .base import CRUDBase

release_crud = CRUDBase[Release](Release)


async def create_release(session: AsyncSession, data: dict) -> Release:
    return await release_crud.create(session, data)


async def list_releases(session: AsyncSession, limit: int = 20, offset: int = 0) -> list[Release]:
    return await release_crud.list(session, limit=limit, offset=offset)

