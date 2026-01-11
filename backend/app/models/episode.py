from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text

from .base import Base


class Episode(Base):
    __tablename__ = "episodes"

    id = Column(Integer, primary_key=True, index=True)
    anime_id = Column(Integer, ForeignKey("anime.id", ondelete="CASCADE"), nullable=False)
    number = Column(Integer, nullable=False)
    title = Column(String(255), nullable=False)
    synopsis = Column(Text)
    aired_at = Column(DateTime(timezone=True))

