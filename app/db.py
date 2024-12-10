# Модуль для инициализации базы данных sqlite3

import os
from pathlib import Path

from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from app.models.base import Base

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

engine = create_async_engine(f"sqlite+aiosqlite:///{BASE_DIR / 'data' / 'db.sqlite3'}")
async_session = async_sessionmaker(engine, class_=AsyncSession)


async def init_db():
    async with engine.begin() as conn:
        logger.info("Initializing database")
        await conn.run_sync(Base.metadata.create_all)
        logger.success("Database is initialized")
