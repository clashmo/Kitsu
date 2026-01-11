from datetime import datetime

from pydantic import BaseModel


class EpisodeBase(BaseModel):
    anime_id: int
    number: int
    title: str
    synopsis: str | None = None
    aired_at: datetime | None = None


class EpisodeCreate(EpisodeBase):
    pass


class EpisodeRead(EpisodeBase):
    id: int

    class Config:
        from_attributes = True

