"""Группы состояний диалогов."""
from aiogram.fsm.state import State, StatesGroup


class Login(StatesGroup):
    """Состояния авторизации."""
    # Состояние начала авторизации
    START = State()
    # Состояние ввода имени пользователя
    username = State()
    # Состояние ввода пароля
    password = State()


class Account(StatesGroup):
    """Состояния личного кабинета."""
    # Состояние начала работы с личным кабинетом
    START = State()


class Settings(StatesGroup):
    """Состояния меню настроек."""
    # Состояние начала работы с меню настроек
    START = State()


class BestStudent(StatesGroup):
    """Состояния показа лучших студентов."""
    # Состояние начала работы с показом лучших студентов
    START = State()


class FindResult(StatesGroup):
    """Состояния показа показателей."""
    # Состояние начала работы с показателем
    START = State()
    # Состояние показа результатов поиска
    SHOW = State()
