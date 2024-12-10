# Обработчик команды /add_playlist - добавить плейлист. Доступен только администратору

from os import getenv

from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from loguru import logger
from dotenv import load_dotenv

from db import async_session
from services.insert_functions import add_playlist_with_songs
from services.select_functions import get_all_genres, get_all_moods
from services.yandex_music_API import get_songs_by_playlist_url

load_dotenv()
router = Router()


class AddPlaylistStates(StatesGroup):
    url = State()
    ru = State()
    genre = State()
    mood = State()
    new = State()
    results = State()


@router.message(Command("add_playlist"))
async def add_playlist(message: types.Message, state: FSMContext):
    if message.from_user.id != int(getenv("ADMIN_ID")):
        logger.debug(f"User {message.from_user.id} tried to use admin command")
        await message.answer("Вы не являетесь администратором бота.")
        return
    logger.debug(f"User {message.from_user.id} added playlist")
    await message.answer(
        "Введите URL плейлиста:",
        reply_markup=types.ReplyKeyboardRemove(),
    )
    await state.set_state(AddPlaylistStates.url)


@router.message(AddPlaylistStates.url)
async def choose_url(message: types.Message, state: FSMContext):
    url = message.text
    logger.debug(f"User {message.from_user.id} want to added playlist {url}")
    await state.update_data(url=url)

    await message.answer(
        "Выбери язык песни (русская/иностранная).",
        reply_markup=types.ReplyKeyboardMarkup(
            keyboard=[
                [types.KeyboardButton(text="Русская")],
                [types.KeyboardButton(text="Иностранная")],
            ],
            resize_keyboard=True,
        ),
    )
    await state.set_state(AddPlaylistStates.ru)


@router.message(AddPlaylistStates.ru)
async def choose_language(message: types.Message, state: FSMContext):
    ru = message.text.lower() == "русская"
    logger.debug(f"User {message.from_user.id} added playlist and chose ru={ru}")
    await state.update_data(ru=ru)

    async with async_session() as session:
        genres = await get_all_genres(session)

    logger.debug(f"Available genres: {genres}")

    await message.answer(
        "Выбери жанр или введи новый:",
        reply_markup=types.ReplyKeyboardMarkup(
            keyboard=[[types.KeyboardButton(text=genre)] for genre in genres],
            resize_keyboard=True,
        ),
    )
    await state.set_state(AddPlaylistStates.genre)


@router.message(AddPlaylistStates.genre)
async def choose_genre(message: types.Message, state: FSMContext):
    genre = message.text
    logger.debug(f"User {message.from_user.id} added playlist and chose genre={genre}")
    await state.update_data(genre=genre)

    async with async_session() as session:
        moods = await get_all_moods(session)

    logger.debug(f"Available moods: {moods}")

    await message.answer(
        "Выбери настроение или введи новое:",
        reply_markup=types.ReplyKeyboardMarkup(
            keyboard=[[types.KeyboardButton(text=mood)] for mood in moods],
            resize_keyboard=True,
        ),
    )
    await state.set_state(AddPlaylistStates.mood)


@router.message(AddPlaylistStates.mood)
async def choose_mood(message: types.Message, state: FSMContext):
    mood = message.text
    logger.debug(f"User {message.from_user.id} added playlist and chose mood={mood}")
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
    await state.set_state(AddPlaylistStates.new)


@router.message(AddPlaylistStates.new)
async def choose_new(message: types.Message, state: FSMContext):
    new = message.text.lower() == "новая"
    logger.debug(f"User {message.from_user.id} chose new={new}")
    await state.update_data(new=new)

    user_data = await state.get_data()
    url = user_data["url"]
    ru = user_data["ru"]
    genre = user_data["genre"]
    mood = user_data["mood"]
    new = user_data["new"]

    playlist_data = {"url": url, "ru": ru, "genre": genre, "mood": mood, "new": new}
    try:
        await message.answer(
            "Ждите, плейлист добавляется...", reply_markup=types.ReplyKeyboardRemove()
        )
        songs_data = get_songs_by_playlist_url(url)
    except Exception as e:
        logger.error(f"Error while getting songs from playlist: {e}")
        await message.answer(
            "Не удалось получить песни из плейлиста.",
            reply_markup=types.ReplyKeyboardRemove(),
        )
        await state.clear()
        return

    async with async_session() as session:
        await add_playlist_with_songs(
            session, playlist_data=playlist_data, songs_data=songs_data
        )

    logger.success(f"Playlist with {len(songs_data)} songs was added successfully.")
    await message.answer(
        f"Плейлист с {len(songs_data)} песнями был успешно добавлен.",
        reply_markup=types.ReplyKeyboardRemove(),
    )

    await state.clear()
