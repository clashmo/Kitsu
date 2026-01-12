from sqlalchemy.ext.asyncio import AsyncSession

from ...crud.refresh_token import get_refresh_token_by_hash
from ...errors import AppError
from ...utils.security import hash_refresh_token


async def logout_user(session: AsyncSession, refresh_token: str) -> None:
    token_hash = hash_refresh_token(refresh_token)
    try:
        stored_token = await get_refresh_token_by_hash(
            session, token_hash, for_update=True
        )
        if stored_token is None:
            return

        stored_token.revoked = True
        await session.flush()
        await session.commit()
    except AppError:
        await session.rollback()
        raise
    except Exception:
        await session.rollback()
        raise
