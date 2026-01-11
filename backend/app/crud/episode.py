import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.episode import Episode
from .base import CRUDBase

episode_crud = CRUDBase[Episode](Episode)


async def get_episodes_by_release(
    session: AsyncSession, release_id: uuid.UUID
) -> list[Episode]:
    stmt = (
        select(Episode)
        .where(Episode.release_id == release_id)
        .order_by(Episode.number.asc())
    )
    result = await session.execute(stmt)
    return list(result.scalars().all())
