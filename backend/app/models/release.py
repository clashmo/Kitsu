from sqlalchemy import Column, DateTime, ForeignKey, Integer, String

from .base import Base


class Release(Base):
    __tablename__ = "releases"

    id = Column(Integer, primary_key=True, index=True)
    anime_id = Column(Integer, ForeignKey("anime.id", ondelete="CASCADE"), nullable=False)
    status = Column(String(64))
    released_at = Column(DateTime(timezone=True))

