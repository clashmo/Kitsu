from sqlalchemy.ext.asyncio import AsyncSession

from ..models.view import View
from .base import CRUDBase

view_crud = CRUDBase[View](View)


async def record_view(session: AsyncSession, data: dict) -> View:
    return await view_crud.create(session, data)


async def list_views(session: AsyncSession, limit: int = 20, offset: int = 0) -> list[View]:
    return await view_crud.list(session, limit=limit, offset=offset)

