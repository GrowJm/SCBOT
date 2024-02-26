"""Настройки проекта."""
import os

from dotenv import load_dotenv

# Загрузка переменных окружения из файла .env
load_dotenv(dotenv_path='infra/.env')

# Получение ссылки на бота из переменной окружения
BOT_LINK = os.getenv('BOT_LINK', default='https://t.me/your_bot_link')

# Получение токена бота из переменной окружения
TOKEN = os.getenv('TOKEN', default='yourbottoken123456789')

# Получение данных для подключения к базе данных PostgreSQL из переменных
# окружения
POSTGRES_USER = str(os.getenv('POSTGRES_USER'))
POSTGRES_PASSWORD = str(os.getenv('POSTGRES_PASSWORD'))
POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_PORT = os.getenv('POSTGRES_PORT')
POSTGRES_DB = str(os.getenv('POSTGRES_DB'))

# Формирование строки подключения к базе данных PostgreSQL
POSTGRES_URI = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
