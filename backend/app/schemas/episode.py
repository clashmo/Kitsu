from datetime import datetime

from pydantic import BaseModel, ConfigDict


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

    model_config = ConfigDict(from_attributes=True)
