from aiogram import Dispatcher

from .start import router as start_router
from .add_playlist import router as add_playlist_router
from .delete_playlist import router as delete_playlist_router
from .help import router as help_router
from .show_playlists import router as show_playlists_router


def register_handlers(dp: Dispatcher):
    dp.include_router(start_router)
    dp.include_router(add_playlist_router)
    dp.include_router(delete_playlist_router)
    dp.include_router(help_router)
    dp.include_router(show_playlists_router)
