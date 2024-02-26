"""Создание бота."""
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from . import settings

# Создание хранилища состояний
storage = MemoryStorage()

# Создание диспетчера для обработки событий
dp = Dispatcher(storage=storage)

# Создание экземпляра бота с использованием токена и настроек парсинга
bot = Bot(token=settings.TOKEN, parse_mode=ParseMode.HTML)
