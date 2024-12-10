# Функции для получения данных из БД

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Playlist


async def get_all_genres(session: AsyncSession):
    result = await session.execute(select(Playlist.genre).distinct())
    genres = result.scalars().all()
    return genres


async def get_all_moods(session: AsyncSession):
    result = await session.execute(select(Playlist.mood).distinct())
    moods = result.scalars().all()
    return moods


async def get_playlist_songs(
    session: AsyncSession, ru: bool, genre: str, mood: str, new: bool
):
    result = await session.execute(
        select(Playlist)
        .where(Playlist.ru == ru)
        .where(Playlist.genre == genre)
        .where(Playlist.mood == mood)
        .where(Playlist.new == new)
    )
    playlist = result.scalars().first()

    if playlist:
        return playlist.songs
    else:
        return None


async def get_all_playlists(session: AsyncSession):
    result = await session.execute(select(Playlist))
    playlists = result.scalars().all()
    return playlists
