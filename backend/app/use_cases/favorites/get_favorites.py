import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from ...crud.favorite import list_favorites
from ...errors import AppError
from ...models.favorite import Favorite


async def get_favorites(
    session: AsyncSession, user_id: uuid.UUID, limit: int, offset: int
) -> list[Favorite]:
    try:
        return await list_favorites(session, user_id=user_id, limit=limit, offset=offset)
    except AppError:
        await session.rollback()
        raise
    except Exception:
        await session.rollback()
        raise
