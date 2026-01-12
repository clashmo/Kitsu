from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from ...config import settings
from ...crud.refresh_token import create_or_rotate_refresh_token
from ...crud.user import create_user_with_password, get_user_by_email
from ...errors import ValidationError
from ...utils.security import (
    create_access_token,
    create_refresh_token,
    hash_refresh_token,
)


@dataclass
class AuthTokens:
    access_token: str
    refresh_token: str


async def issue_tokens(session: AsyncSession, user_id: uuid.UUID) -> AuthTokens:
    access_token = create_access_token({"sub": str(user_id)})
    refresh_token = create_refresh_token()
    token_hash = hash_refresh_token(refresh_token)
    expires_at = datetime.now(timezone.utc) + timedelta(
        days=settings.refresh_token_expire_days
    )
    await create_or_rotate_refresh_token(session, user_id, token_hash, expires_at)
    await session.commit()
    return AuthTokens(access_token=access_token, refresh_token=refresh_token)


async def register_user(session: AsyncSession, email: str, password: str) -> AuthTokens:
    existing_user = await get_user_by_email(session, email)
    if existing_user:
        raise ValidationError("Email already registered")

    user = await create_user_with_password(session, email, password)
    return await issue_tokens(session, user.id)
