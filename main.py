# Точка входа в приложение

import asyncio
from aiogram import Bot, Dispatcher

from app.bot import setup_bot
from app.db import init_db
from loguru import logger
from app.handlers import register_handlers


async def main():
    logger.info("Initializing bot")
    bot: Bot = setup_bot()
    logger.success("Bot is initialized")
    dp = Dispatcher()

    await init_db()

    logger.info("Registering handlers")
    register_handlers(dp)
    logger.success("Handlers are registered")

    logger.info("Starting bot")
    try:
        await dp.start_polling(bot)
    finally:
        logger.info("Closing bot session")
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
