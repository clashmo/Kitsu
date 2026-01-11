from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..crud.user import (
    authenticate_user,
    create_user_with_password,
    get_user_by_email,
)
from ..dependencies import get_db
from ..schemas.auth import TokenResponse, UserLogin, UserRegister
from ..utils.security import create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])


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
    await db.commit()
    await db.refresh(user)

    access_token = create_access_token({"sub": str(user.id)})
    return TokenResponse(access_token=access_token)


@router.post("/login", response_model=TokenResponse)
async def login(payload: UserLogin, db: AsyncSession = Depends(get_db)) -> TokenResponse:
    user = await authenticate_user(db, payload.email, payload.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    access_token = create_access_token({"sub": str(user.id)})
    return TokenResponse(access_token=access_token)
