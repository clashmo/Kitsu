from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..crud.refresh_token import get_refresh_token_by_hash, revoke_refresh_token
from ..crud.user import authenticate_user
from ..dependencies import get_db
from ..schemas.auth import (
    LogoutRequest,
    RefreshTokenRequest,
    TokenResponse,
    UserLogin,
    UserRegister,
)
from ..use_cases.auth.register_user import issue_tokens, register_user
from ..utils.security import (
    hash_refresh_token,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(
    payload: UserRegister, db: AsyncSession = Depends(get_db)
) -> TokenResponse:
    tokens = await register_user(db, payload.email, payload.password)
    return TokenResponse(
        access_token=tokens.access_token, refresh_token=tokens.refresh_token
    )


@router.post("/login", response_model=TokenResponse)
async def login(payload: UserLogin, db: AsyncSession = Depends(get_db)) -> TokenResponse:
    user = await authenticate_user(db, payload.email, payload.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    tokens = await issue_tokens(db, user.id)
    return TokenResponse(
        access_token=tokens.access_token, refresh_token=tokens.refresh_token
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    payload: RefreshTokenRequest, db: AsyncSession = Depends(get_db)
) -> TokenResponse:
    token_hash = hash_refresh_token(payload.refresh_token)
    stored_token = await get_refresh_token_by_hash(db, token_hash, for_update=True)
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
    tokens = await issue_tokens(db, stored_token.user_id)
    return TokenResponse(
        access_token=tokens.access_token, refresh_token=tokens.refresh_token
    )


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    payload: LogoutRequest, db: AsyncSession = Depends(get_db)
) -> None:
    token_hash = hash_refresh_token(payload.refresh_token)
    stored_token = await get_refresh_token_by_hash(db, token_hash, for_update=True)
    if stored_token is None:
        return

    await revoke_refresh_token(db, stored_token.user_id)
    await db.commit()
