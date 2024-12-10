# Модуль описывает модель песни и связывающую таблицу (песни-плейлисты)

from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import Base

# Связывающая таблица для "многие ко многим"
playlist_song_association = Table(
    "playlist_song",
    Base.metadata,
    Column("playlist_id", Integer, ForeignKey("playlists.id"), primary_key=True),
    Column("song_id", Integer, ForeignKey("songs.id"), primary_key=True),
)


class Song(Base):
    __tablename__ = "songs"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    artists = Column(String, nullable=False)
    url = Column(String, nullable=False)

    # Связь с плейлистами через связывающую таблицу
    playlists = relationship(
        "Playlist",
        secondary=playlist_song_association,
        back_populates="songs",
        lazy="selectin",
    )
