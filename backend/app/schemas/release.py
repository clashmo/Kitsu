from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ReleaseBase(BaseModel):
    anime_id: int
    status: str | None = None
    released_at: datetime | None = None


class ReleaseCreate(ReleaseBase):
    pass


class ReleaseRead(ReleaseBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
