from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..dependencies import get_db
from ..schemas.user import UserCreate, UserRead

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=list[UserRead])
async def list_users(db: AsyncSession = Depends(get_db)) -> list[UserRead]:
    # TODO: Replace with real database query.
    return []


@router.post("/", response_model=UserRead, status_code=201)
async def create_user(payload: UserCreate, db: AsyncSession = Depends(get_db)) -> UserRead:
    # TODO: Persist user to database.
    return UserRead(id=0, email=payload.email, is_active=True, created_at=datetime.now())


@router.get("/{user_id}", response_model=UserRead)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)) -> UserRead:
    # TODO: Load user from database.
    return UserRead(
        id=user_id,
        email="placeholder@example.com",
        is_active=True,
        created_at=datetime.now(),
    )

