# Обработчик команды /delete_playlist - удалить плейлист. Доступен только администратору

from os import getenv

from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from loguru import logger
from dotenv import load_dotenv

from db import async_session
from services.delete_functions import delete_playlist_by_id
from services.select_functions import get_all_playlists

load_dotenv()
router = Router()


class DeletePlaylistStates(StatesGroup):
    id = State()
    results = State()


@router.message(Command("delete_playlist"))
async def delete_playlist(message: types.Message, state: FSMContext):
    if message.from_user.id != int(getenv("ADMIN_ID")):
        logger.debug(f"User {message.from_user.id} tried to use admin command")
        await message.answer("Вы не являетесь администратором бота.")
        return
    logger.debug(f"User {message.from_user.id} deleted playlist")
    async with async_session() as session:
        playlists = await get_all_playlists(session)
    current_message = "Доступные плейлисты для удаления:"
    for playlist in playlists:
        current_message += f"\nid: {playlist.id}\nurl: {playlist.url}\nru: {playlist.ru}\ngenre: {playlist.genre}\nmood: {playlist.mood}\nnew: {playlist.new}\n\n"
    await message.answer(
        current_message,
        reply_markup=types.ReplyKeyboardRemove(),
    )
    await message.answer(
        "Введите id плейлиста (введите 0 для отмены):",
        reply_markup=types.ReplyKeyboardMarkup(
            keyboard=[[types.KeyboardButton(text=str(p.id))] for p in playlists],
            resize_keyboard=True,
        ),
    )
    await state.set_state(DeletePlaylistStates.id)


@router.message(DeletePlaylistStates.id)
async def choose_id(message: types.Message, state: FSMContext):
    id = int(message.text)
    logger.debug(f"User {message.from_user.id} want to delete playlist {id}")

    async with async_session() as session:
        await delete_playlist_by_id(session, id)

    logger.success(f"Playlist with id={id} was deleted successfully.")
    await message.answer(
        f"Плейлист с id={id} успешно удален.", reply_markup=types.ReplyKeyboardRemove()
    )
    await state.clear()
