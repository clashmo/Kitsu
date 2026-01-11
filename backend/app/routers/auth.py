import uuid
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..config import settings
from ..crud.refresh_token import (
    create_refresh_token as create_refresh_token_record,
    get_refresh_token_by_hash,
    revoke_all_user_tokens,
    revoke_refresh_token,
)
from ..crud.user import (
    authenticate_user,
    create_user_with_password,
    get_user_by_email,
)
from ..dependencies import get_db
from ..schemas.auth import (
    RefreshTokenRequest,
    TokenPairResponse,
    UserLogin,
    UserRegister,
)
from ..utils.security import (
    TokenExpiredError,
    TokenInvalidError,
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
    hash_refresh_token,
    verify_refresh_token,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register",
    response_model=TokenPairResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    payload: UserRegister, db: AsyncSession = Depends(get_db)
) -> TokenPairResponse:
    existing_user = await get_user_by_email(db, payload.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    user = await create_user_with_password(db, payload.email, payload.password)
    await revoke_all_user_tokens(db, user.id)

    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token(user.id)
    refresh_expires_at = datetime.now(timezone.utc) + timedelta(
        days=settings.refresh_token_expire_days
    )
    hashed_refresh_token = hash_refresh_token(refresh_token)
    await create_refresh_token_record(
        db, user.id, hashed_refresh_token, refresh_expires_at
    )
    await db.commit()

    return TokenPairResponse(
        access_token=access_token, refresh_token=refresh_token
    )


@router.post("/login", response_model=TokenPairResponse)
async def login(
    payload: UserLogin, db: AsyncSession = Depends(get_db)
) -> TokenPairResponse:
    user = await authenticate_user(db, payload.email, payload.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    await revoke_all_user_tokens(db, user.id)

    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token(user.id)
    refresh_expires_at = datetime.now(timezone.utc) + timedelta(
        days=settings.refresh_token_expire_days
    )
    hashed_refresh_token = hash_refresh_token(refresh_token)
    await create_refresh_token_record(
        db, user.id, hashed_refresh_token, refresh_expires_at
    )
    await db.commit()

    return TokenPairResponse(
        access_token=access_token, refresh_token=refresh_token
    )


@router.post("/refresh", response_model=TokenPairResponse)
async def refresh_tokens(
    payload: RefreshTokenRequest, db: AsyncSession = Depends(get_db)
) -> TokenPairResponse:
    raw_refresh_token = payload.refresh_token
    try:
        token_payload = decode_refresh_token(raw_refresh_token)
    except TokenExpiredError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token has expired",
        ) from None
    except TokenInvalidError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        ) from None

    hashed_refresh_token = hash_refresh_token(raw_refresh_token)
    stored_token = await get_refresh_token_by_hash(db, hashed_refresh_token)
    if stored_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )

    try:
        subject = token_payload["sub"]
        user_id = uuid.UUID(str(subject))
    except (KeyError, ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token payload",
        ) from None

    if stored_token.revoked:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Refresh token revoked"
        )
    if stored_token.expires_at <= datetime.now(timezone.utc):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token has expired",
        )
    if stored_token.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Refresh token reuse detected",
        )
    if not verify_refresh_token(raw_refresh_token, stored_token.token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )

    await revoke_refresh_token(db, stored_token.id)

    access_token = create_access_token({"sub": str(user_id)})
    new_refresh_token = create_refresh_token(user_id)
    new_refresh_expires_at = datetime.now(timezone.utc) + timedelta(
        days=settings.refresh_token_expire_days
    )
    new_hashed_refresh_token = hash_refresh_token(new_refresh_token)
    await create_refresh_token_record(
        db, user_id, new_hashed_refresh_token, new_refresh_expires_at
    )
    await db.commit()

    return TokenPairResponse(
        access_token=access_token, refresh_token=new_refresh_token
    )


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    payload: RefreshTokenRequest, db: AsyncSession = Depends(get_db)
) -> Response:
    raw_refresh_token = payload.refresh_token
    try:
        token_payload = decode_refresh_token(raw_refresh_token)
    except TokenExpiredError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token has expired",
        ) from None
    except TokenInvalidError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        ) from None

    hashed_refresh_token = hash_refresh_token(raw_refresh_token)
    stored_token = await get_refresh_token_by_hash(db, hashed_refresh_token)
    if stored_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )

    try:
        subject = token_payload["sub"]
        user_id = uuid.UUID(str(subject))
    except (KeyError, ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token payload",
        ) from None

    if stored_token.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Refresh token reuse detected",
        )

    if stored_token.revoked:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    await revoke_refresh_token(db, stored_token.id)
    await db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
