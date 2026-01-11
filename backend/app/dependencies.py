import uuid
from collections.abc import AsyncGenerator
from typing import Literal

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from .database import get_session
from .models.user import User
from .utils.security import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def _credentials_exception() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )


async def _load_user_or_raise(
    db: AsyncSession, user_uuid: uuid.UUID, exc: HTTPException
) -> User:
    user = await db.get(User, user_uuid)
    if user is None:
        raise exc
    return user


async def _get_user_from_token(
    token: str,
    *,
    expected_type: Literal["access", "refresh"],
    db: AsyncSession,
    exc: HTTPException,
) -> User:
    try:
        payload = decode_token(token, expected_type=expected_type)
        user_id = payload.get("sub")
        if user_id is None:
            raise exc
        user_uuid = uuid.UUID(user_id)
    except (jwt.InvalidTokenError, ValueError):
        raise exc
    return await _load_user_or_raise(db, user_uuid, exc)


def _ensure_active_user(user: User, exc: HTTPException) -> User:
    if not user.is_active:
        raise exc
    return user


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async for session in get_session():
        yield session


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)
) -> User:
    return await _get_user_from_token(
        token,
        expected_type="access",
        db=db,
        exc=_credentials_exception(),
    )


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    return _ensure_active_user(
        current_user,
        HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user"
        ),
    )
