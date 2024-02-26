"""Команды, доступные пользователю из меню в любой момент."""
from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot):
    """Установка команд."""
    # Список команд, доступных пользователю из меню в любой момент
    commands = [
        # Команда для начала работы с ботом
        BotCommand(
            command='start',
            description='Начало работы'
        ),

        # Команда для перехода в личный кабинет пользователя
        BotCommand(
            command='account',
            description='Личный кабинет'
        ),

        # Команда для получения информации о проекте
        BotCommand(
            command='info',
            description='О проекте'
        ),

        # Команда для сброса всех данных пользователя
        BotCommand(
            command='reset_all',
            description='Сбросить все данные'
        ),
    ]

    # Установка команд в Telegram API
    await bot.set_my_commands(commands, BotCommandScopeDefault())
