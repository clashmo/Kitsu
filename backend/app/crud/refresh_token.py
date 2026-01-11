import uuid
from datetime import datetime

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.refresh_token import RefreshToken


async def get_active_refresh_token(
    session: AsyncSession, user_id: uuid.UUID
) -> RefreshToken | None:
    stmt = select(RefreshToken).where(
        RefreshToken.user_id == user_id, RefreshToken.revoked.is_(False)
    )
    result = await session.execute(stmt)
    return result.scalars().first()


async def get_refresh_token_by_hash(
    session: AsyncSession, hashed_token: str
) -> RefreshToken | None:
    stmt = select(RefreshToken).where(RefreshToken.token == hashed_token)
    result = await session.execute(stmt)
    return result.scalars().first()


async def create_refresh_token(
    session: AsyncSession,
    user_id: uuid.UUID,
    hashed_token: str,
    expires_at: datetime,
) -> RefreshToken:
    refresh_token = RefreshToken(
        user_id=user_id, token=hashed_token, expires_at=expires_at
    )
    session.add(refresh_token)
    await session.flush()
    return refresh_token


async def revoke_refresh_token(session: AsyncSession, token_id: uuid.UUID) -> None:
    stmt = (
        update(RefreshToken)
        .where(RefreshToken.id == token_id, RefreshToken.revoked.is_(False))
        .values(revoked=True)
    )
    await session.execute(stmt)


async def revoke_all_user_tokens(session: AsyncSession, user_id: uuid.UUID) -> None:
    stmt = (
        update(RefreshToken)
        .where(RefreshToken.user_id == user_id, RefreshToken.revoked.is_(False))
        .values(revoked=True)
    )
    await session.execute(stmt)
