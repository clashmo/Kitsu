from datetime import datetime, timedelta, timezone
import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..config import settings
from ..crud.refresh_token import (
    create_or_rotate_refresh_token,
    get_refresh_token_by_hash,
    revoke_refresh_token,
)
from ..crud.user import (
    authenticate_user,
    create_user_with_password,
    get_user_by_email,
)
from ..dependencies import get_db
from ..schemas.auth import (
    LogoutRequest,
    RefreshTokenRequest,
    TokenResponse,
    UserLogin,
    UserRegister,
)
from ..utils.security import (
    create_access_token,
    create_refresh_token,
    hash_refresh_token,
)

router = APIRouter(prefix="/auth", tags=["auth"])


async def _issue_tokens(db: AsyncSession, user_id: uuid.UUID) -> TokenResponse:
    access_token = create_access_token({"sub": str(user_id)})
    refresh_token = create_refresh_token(user_id)
    token_hash = hash_refresh_token(refresh_token)
    expires_at = datetime.now(timezone.utc) + timedelta(
        days=settings.refresh_token_expire_days
    )
    await create_or_rotate_refresh_token(db, user_id, token_hash, expires_at)
    await db.commit()
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(
    payload: UserRegister, db: AsyncSession = Depends(get_db)
) -> TokenResponse:
    existing_user = await get_user_by_email(db, payload.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    user = await create_user_with_password(db, payload.email, payload.password)
    await db.flush()

    return await _issue_tokens(db, user.id)


@router.post("/login", response_model=TokenResponse)
async def login(payload: UserLogin, db: AsyncSession = Depends(get_db)) -> TokenResponse:
    user = await authenticate_user(db, payload.email, payload.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    return await _issue_tokens(db, user.id)


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    payload: RefreshTokenRequest, db: AsyncSession = Depends(get_db)
) -> TokenResponse:
    token_hash = hash_refresh_token(payload.refresh_token)
    stored_token = await get_refresh_token_by_hash(db, token_hash)
    if stored_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
        )
    if stored_token.revoked:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Refresh token has been revoked"
        )
    if stored_token.expires_at <= datetime.now(timezone.utc):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token has expired"
        )
    return await _issue_tokens(db, stored_token.user_id)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    payload: LogoutRequest, db: AsyncSession = Depends(get_db)
) -> None:
    token_hash = hash_refresh_token(payload.refresh_token)
    stored_token = await get_refresh_token_by_hash(db, token_hash)
    if stored_token is None:
        return

    await revoke_refresh_token(db, stored_token.user_id)
    await db.commit()
