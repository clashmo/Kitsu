import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.favorite import Favorite
from .base import CRUDBase

favorite_crud = CRUDBase[Favorite](Favorite)


async def add_favorite(
    session: AsyncSession, user_id: uuid.UUID, anime_id: uuid.UUID
) -> Favorite:
    stmt = select(Favorite).where(
        Favorite.user_id == user_id, Favorite.anime_id == anime_id
    )
    result = await session.execute(stmt)
    existing = result.scalar_one_or_none()
    if existing:
        raise ValueError("Favorite already exists")

    favorite = Favorite(user_id=user_id, anime_id=anime_id)
    session.add(favorite)
    await session.flush()
    return favorite


async def remove_favorite(
    session: AsyncSession, user_id: uuid.UUID, anime_id: uuid.UUID
) -> None:
    stmt = select(Favorite).where(
        Favorite.user_id == user_id, Favorite.anime_id == anime_id
    )
    result = await session.execute(stmt)
    favorite = result.scalar_one_or_none()
    if favorite is None:
        raise LookupError("Favorite not found")

    session.delete(favorite)
    await session.flush()


async def list_favorites(
    session: AsyncSession, user_id: uuid.UUID, limit: int, offset: int
) -> list[Favorite]:
    stmt = (
        select(Favorite)
        .where(Favorite.user_id == user_id)
        .order_by(Favorite.created_at.desc())
        .limit(limit)
        .offset(offset)
    )
    result = await session.execute(stmt)
    return list(result.scalars().all())
