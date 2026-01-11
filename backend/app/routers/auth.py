from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..dependencies import get_db
from ..schemas.auth import Credentials, Token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=Token)
async def login(payload: Credentials, db: AsyncSession = Depends(get_db)) -> Token:
    # TODO: Implement authentication and token issuance.
    if not payload.username or not payload.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials")

    return Token(access_token="stub-token")


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(db: AsyncSession = Depends(get_db)) -> None:
    # TODO: Invalidate token/session when authentication is implemented.
    return None

