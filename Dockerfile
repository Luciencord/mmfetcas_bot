# Используем официальный Python образ
FROM python:3.11

ENV PYTHONUNBUFFERED=1

# Устанавливаем зависимости
RUN apt-get update

RUN pip install --upgrade pip "poetry==1.8.3"

# Запускаем в контейнере => виртуальное окружение как таковое не нужно
RUN poetry config virtualenvs.create false

# Устанавливаем рабочую директорию
WORKDIR /bot

# Копируем pyproject.toml и poetry.lock и устанавливаем зависимости
COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock

# Устанавливаем зависимости проекта
RUN poetry install --no-root

# Копируем исходный код
COPY . /bot/

# Выполняем миграции, добавляем CRON задачи и запускаем приложение
CMD ["poetry", "run", "python", "main.py"]
