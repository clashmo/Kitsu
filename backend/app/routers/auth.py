from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..crud.user import get_user_by_email
from ..dependencies import _ensure_active_user, _get_user_from_token, get_db
from ..models.user import User
from ..routers.users import _create_user_or_raise
from ..schemas.auth import Credentials, RefreshTokenRequest, Token
from ..schemas.user import UserCreate, UserRead
from ..utils.security import (
    create_access_token,
    create_refresh_token,
    verify_password,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(payload: UserCreate, db: AsyncSession = Depends(get_db)) -> UserRead:
    user = await _create_user_or_raise(payload, db)
    return UserRead.model_validate(user)


@router.post("/login", response_model=Token)
async def login(payload: Credentials, db: AsyncSession = Depends(get_db)) -> Token:
    user = await get_user_by_email(db, payload.email)
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user",
        )

    return Token(
        access_token=create_access_token(user.id),
        refresh_token=create_refresh_token(user.id),
    )


@router.post("/refresh", response_model=Token)
async def refresh(
    payload: RefreshTokenRequest, db: AsyncSession = Depends(get_db)
) -> Token:
    invalid_refresh_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid refresh token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    user = await _get_user_from_token(
        payload.refresh_token,
        expected_type="refresh",
        db=db,
        exc=invalid_refresh_exc,
    )
    _ensure_active_user(
        user,
        HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user"
        ),
    )

    return Token(access_token=create_access_token(user.id))
