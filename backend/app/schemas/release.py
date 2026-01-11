from datetime import datetime

from pydantic import BaseModel


class ReleaseBase(BaseModel):
    anime_id: int
    status: str | None = None
    released_at: datetime | None = None


class ReleaseCreate(ReleaseBase):
    pass


class ReleaseRead(ReleaseBase):
    id: int

    class Config:
        from_attributes = True

