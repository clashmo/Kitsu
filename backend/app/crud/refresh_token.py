from datetime import datetime
import uuid

from sqlalchemy import select
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
    session: AsyncSession,
    user_id: uuid.UUID,
    token_hash: str | None = None,
    delete: bool = False,
) -> RefreshToken | None:
    """
    Revoke a refresh token for a user. When token_hash is provided, that token is
    targeted; otherwise the most recently created token for the user is used.
    If delete is True, the matched token row is removed instead of being marked revoked.
    """
    stmt = select(RefreshToken).where(RefreshToken.user_id == user_id)
    if token_hash is not None:
        stmt = stmt.where(RefreshToken.token_hash == token_hash)
    else:
        stmt = stmt.order_by(RefreshToken.created_at.desc()).limit(1)

    result = await session.execute(stmt)
    token = result.scalars().first()
    if token is None:
        return None

    if delete:
        await session.delete(token)
    else:
        token.revoked = True
    await session.flush()
    return token
