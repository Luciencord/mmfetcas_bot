# Обработчик команды /help - выводит список всех команд

from os import getenv

from aiogram import Router, types
from aiogram.filters import Command
from dotenv import load_dotenv
from loguru import logger

load_dotenv()
router = Router()


@router.message(Command("help"))
async def help_handler(message: types.Message):
    logger.debug(f"User {message.from_user.id} used help command")
    if message.from_user.id != int(getenv("ADMIN_ID")):
        await message.answer("Все команды:\n/start - подобрать песню\n/help - помощь")
        return
    await message.answer(
        "Все команды:\n/start - подобрать песню\n/help - помощь\n/add_playlist - добавить плейлист\n/delete_playlist - удалить плейлист\n/show_playlists - показать все плейлисты"
    )
