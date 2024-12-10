# Обработчик команды /start - получает песню по выбранным параметрам

import random

from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from loguru import logger

from db import async_session
from services.select_functions import get_all_genres, get_all_moods, get_playlist_songs

router = Router()


class SongFilterStates(StatesGroup):
    ru = State()
    genre = State()
    mood = State()
    new = State()
    results = State()


# Стартовый обработчик
@router.message(Command("start"))
async def start_handler(message: types.Message, state: FSMContext):
    logger.debug(f"User {message.from_user.id} started the bot")
    await message.answer(
        "Привет! Я помогу тебе выбрать песню. Выбери язык песни (русская/иностранная).",
        reply_markup=types.ReplyKeyboardMarkup(
            keyboard=[
                [types.KeyboardButton(text="Русская")],
                [types.KeyboardButton(text="Иностранная")],
            ],
            resize_keyboard=True,
        ),
    )
    await state.set_state(SongFilterStates.ru)


@router.message(SongFilterStates.ru)
async def choose_language(message: types.Message, state: FSMContext):
    ru = message.text.lower() == "русская"
    logger.debug(f"User {message.from_user.id} chose ru={ru}")
    await state.update_data(ru=ru)

    async with async_session() as session:
        genres = await get_all_genres(session)

    logger.debug(f"Available genres: {genres}")

    await message.answer(
        "Выбери жанр:",
        reply_markup=types.ReplyKeyboardMarkup(
            keyboard=[[types.KeyboardButton(text=genre)] for genre in genres],
            resize_keyboard=True,
        ),
    )
    await state.set_state(SongFilterStates.genre)


@router.message(SongFilterStates.genre)
async def choose_genre(message: types.Message, state: FSMContext):
    genre = message.text
    logger.debug(f"User {message.from_user.id} chose genre={genre}")
    await state.update_data(genre=genre)

    async with async_session() as session:
        moods = await get_all_moods(session)

    logger.debug(f"Available moods: {moods}")

    await message.answer(
        "Выбери настроение:",
        reply_markup=types.ReplyKeyboardMarkup(
            keyboard=[[types.KeyboardButton(text=mood)] for mood in moods],
            resize_keyboard=True,
        ),
    )
    await state.set_state(SongFilterStates.mood)


@router.message(SongFilterStates.mood)
async def choose_mood(message: types.Message, state: FSMContext):
    mood = message.text
    logger.debug(f"User {message.from_user.id} chose mood={mood}")
    await state.update_data(mood=mood)

    await message.answer(
        "Выбери, старая или новая песня:",
        reply_markup=types.ReplyKeyboardMarkup(
            keyboard=[
                [types.KeyboardButton(text="Старая")],
                [types.KeyboardButton(text="Новая")],
            ],
            resize_keyboard=True,
        ),
    )
    await state.set_state(SongFilterStates.new)


@router.message(SongFilterStates.new)
async def choose_new(message: types.Message, state: FSMContext):
    new = message.text.lower() == "новая"
    logger.debug(f"User {message.from_user.id} chose new={new}")
    await state.update_data(new=new)

    # Получаем данные, которые были собраны
    user_data = await state.get_data()
    ru = user_data["ru"]
    genre = user_data["genre"]
    mood = user_data["mood"]
    new = user_data["new"]

    async with async_session() as session:
        songs = await get_playlist_songs(session, ru, genre, mood, new)

    if songs:
        logger.success(f"Songs found: {len(songs)}")
        random_songs = random.sample(songs, 3)
        messages = [
            f"{song.title} - {song.artists}: {song.url}" for song in random_songs
        ]
        await message.answer(
            "\n".join(messages), reply_markup=types.ReplyKeyboardRemove()
        )
    else:
        logger.warning(
            f"No songs found for: ru={ru}, genre={genre}, mood={mood}, new={new}"
        )
        await message.answer(
            "Не удалось найти песни по вашим критериям.",
            reply_markup=types.ReplyKeyboardRemove(),
        )

    # Завершаем диалог
    await state.clear()
