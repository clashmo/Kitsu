from sqlalchemy.ext.asyncio import AsyncSession

from ..models.episode import Episode
from .base import CRUDBase

episode_crud = CRUDBase[Episode](Episode)


async def create_episode(session: AsyncSession, data: dict) -> Episode:
    return await episode_crud.create(session, data)


async def list_episodes(session: AsyncSession, limit: int = 20, offset: int = 0) -> list[Episode]:
    return await episode_crud.list(session, limit=limit, offset=offset)

