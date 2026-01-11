from sqlalchemy.ext.asyncio import AsyncSession

from ..models.user import User
from .base import CRUDBase

user_crud = CRUDBase[User](User)


async def create_user(session: AsyncSession, data: dict) -> User:
    # TODO: Add validation and hashing logic.
    return await user_crud.create(session, data)


async def get_user(session: AsyncSession, user_id: int) -> User | None:
    return await user_crud.get(session, user_id)

