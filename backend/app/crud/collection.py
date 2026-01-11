from sqlalchemy.ext.asyncio import AsyncSession

from ..models.collection import Collection
from .base import CRUDBase

collection_crud = CRUDBase[Collection](Collection)


async def create_collection(session: AsyncSession, data: dict) -> Collection:
    return await collection_crud.create(session, data)


async def list_collections(session: AsyncSession, limit: int = 20, offset: int = 0) -> list[Collection]:
    return await collection_crud.list(session, limit=limit, offset=offset)

