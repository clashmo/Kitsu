from datetime import datetime
import uuid

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.refresh_token import RefreshToken


async def create_or_rotate_refresh_token(
    session: AsyncSession, user_id: uuid.UUID, token_hash: str, expires_at: datetime
) -> RefreshToken:
    refresh_token = RefreshToken(
        user_id=user_id,
        token_hash=token_hash,
        expires_at=expires_at,
        revoked=False,
    )
    session.add(refresh_token)
    await session.flush()
    return refresh_token


async def get_refresh_token_by_hash(
    session: AsyncSession, token_hash: str, *, for_update: bool = False
) -> RefreshToken | None:
    stmt = select(RefreshToken).where(RefreshToken.token_hash == token_hash)
    if for_update:
        stmt = stmt.with_for_update()

    result = await session.execute(stmt)
    return result.scalars().first()


async def revoke_refresh_token(
    session: AsyncSession, user_id: uuid.UUID
) -> RefreshToken | None:
    latest_result = await session.execute(
        select(RefreshToken)
        .where(RefreshToken.user_id == user_id)
        .order_by(RefreshToken.created_at.desc())
        .limit(1)
    )
    latest_token = latest_result.scalars().first()
    if latest_token is None:
        return None

    await session.execute(
        update(RefreshToken).where(RefreshToken.user_id == user_id).values(revoked=True)
    )
    await session.flush()
    return latest_token
