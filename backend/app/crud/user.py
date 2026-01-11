from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.user import User
from .base import CRUDBase

user_crud = CRUDBase[User](User)


async def create_user(session: AsyncSession, data: dict) -> User:
    # TODO: Add validation and hashing logic.
    return await user_crud.create(session, data)


async def get_user(session: AsyncSession, user_id: int) -> User | None:
    return await user_crud.get(session, user_id)


async def get_user_by_email(session: AsyncSession, email: str) -> User | None:
    stmt = select(User).where(User.email == email)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()
