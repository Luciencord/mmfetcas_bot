# Модуль для инициализации бота

from aiogram import Bot
from dotenv import load_dotenv
from os import getenv

load_dotenv()


def setup_bot() -> Bot:
    return Bot(token=getenv("BOT_TOKEN"))
