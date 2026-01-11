from .anime import anime_crud
from .collection import collection_crud
from .favorite import favorite_crud
from .episode import episode_crud
from .release import release_crud
from .user import user_crud
from .view import view_crud

__all__ = [
    "user_crud",
    "anime_crud",
    "release_crud",
    "episode_crud",
    "collection_crud",
    "favorite_crud",
    "view_crud",
]
