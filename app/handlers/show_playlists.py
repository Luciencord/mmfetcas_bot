# Обработчик команды /show_playlists - просмотреть список всех плейлистов. Доступен только администратору

from os import getenv

from aiogram import Router, types
from aiogram.filters import Command
from loguru import logger
from dotenv import load_dotenv

from db import async_session
from services.select_functions import get_all_playlists

load_dotenv()
router = Router()


@router.message(Command("show_playlists"))
async def show_playlists(message: types.Message):
    if message.from_user.id != int(getenv("ADMIN_ID")):
        logger.debug(f"User {message.from_user.id} tried to use admin command")
        await message.answer("Вы не являетесь администратором бота.")
        return
    logger.debug(f"User {message.from_user.id} wanted to see playlists")
    async with async_session() as session:
        playlists = await get_all_playlists(session)
    current_message = "Доступные плейлисты:"
    for playlist in playlists:
        current_message += f"\nid: {playlist.id}\nurl: {playlist.url}\nru: {playlist.ru}\ngenre: {playlist.genre}\nmood: {playlist.mood}\nnew: {playlist.new}\n\n"
    await message.answer(
        current_message,
        reply_markup=types.ReplyKeyboardRemove(),
    )
