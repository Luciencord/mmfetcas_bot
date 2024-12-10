# Модуль инициализации клиента яндекс музыки

import os

from dotenv import load_dotenv
from loguru import logger
from yandex_music import Client

load_dotenv()
YANDEX_TOKEN = os.getenv("YANDEX_TOKEN")


client = Client(YANDEX_TOKEN).init()
logger.debug("Yandex music client is initialized")
