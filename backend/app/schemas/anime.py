from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AnimeBase(BaseModel):
    title: str
    slug: str
    synopsis: str | None = None


class AnimeCreate(AnimeBase):
    pass


class AnimeRead(AnimeBase):
    id: int
    created_at: datetime
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
