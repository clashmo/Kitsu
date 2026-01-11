from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from ..crud.anime import get_anime_by_id
from ..crud.favorite import add_favorite, list_favorites, remove_favorite
from ..dependencies import get_current_user, get_db
from ..models.user import User
from ..schemas.favorite import FavoriteCreate, FavoriteRead

router = APIRouter(prefix="/favorites", tags=["favorites"])


@router.get("/", response_model=list[FavoriteRead])
async def get_favorites(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[FavoriteRead]:
    return await list_favorites(db, user_id=current_user.id, limit=limit, offset=offset)


@router.post("/", response_model=FavoriteRead, status_code=status.HTTP_201_CREATED)
async def create_favorite(
    payload: FavoriteCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> FavoriteRead:
    anime = await get_anime_by_id(db, payload.anime_id)
    if anime is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Anime not found"
        )

    try:
        favorite = await add_favorite(db, user_id=current_user.id, anime_id=payload.anime_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Favorite already exists"
        ) from None
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Favorite already exists"
        ) from None

    await db.commit()
    await db.refresh(favorite)
    return favorite


@router.delete("/{anime_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_favorite(
    anime_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    try:
        await remove_favorite(db, user_id=current_user.id, anime_id=anime_id)
    except LookupError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Favorite not found"
        ) from None

    await db.commit()
