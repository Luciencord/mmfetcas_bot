# Функции для удаления данных из БД

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from app.models.playlist import Playlist


async def delete_playlist_by_id(session: AsyncSession, playlist_id: int):
    # Найти плейлист
    query = select(Playlist).where(Playlist.id == playlist_id)
    result = await session.execute(query)
    playlist = result.scalar_one_or_none()

    if not playlist:
        return

    await session.delete(playlist)
    await session.commit()
