# Функции для добавления данных в БД

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.playlist import Playlist
from app.models.song import Song


async def add_playlist_with_songs(
    session: AsyncSession, playlist_data: dict, songs_data: list[dict]
):
    """
    Добавляет плейлист и песни к нему.

    Args:
        session: Сессия для работы с базой данных.
        playlist_data: Словарь с данными для плейлиста.
            Пример: {"ru": True, "genre": "Рок", "mood": "Веселое", "new": True, "url": "http://playlist.url"}
        songs_data: Список словарей с данными для песен.
            Пример: [{"title": "Song 1", "artists": "Artist 1, Artist 2", "url": "http://song1.url"}, ...]
    """
    playlist = Playlist(**playlist_data)

    songs = []

    for song_data in songs_data:
        result = await session.execute(
            select(Song).where(
                Song.title == song_data["title"], Song.artists == song_data["artists"]
            )
        )
        song = result.scalars().first()

        if not song:
            song = Song(**song_data)
            session.add(song)
        songs.append(song)

    playlist.songs = songs
    session.add(playlist)
    await session.commit()
