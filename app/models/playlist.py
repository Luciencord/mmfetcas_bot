# Модуль описывает модель плейлиста

from sqlalchemy import Column, Integer, String, Table, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from app.models.base import Base
from .song import playlist_song_association


class Playlist(Base):
    __tablename__ = "playlists"

    id = Column(Integer, primary_key=True)
    url = Column(String, nullable=False)
    ru = Column(Boolean, nullable=False)
    genre = Column(String, nullable=False)
    mood = Column(String, nullable=False)
    new = Column(Boolean, nullable=False)

    # Связь с песнями через связывающую таблицу
    songs = relationship(
        "Song",
        secondary=playlist_song_association,
        back_populates="playlists",
        lazy="selectin",
    )
