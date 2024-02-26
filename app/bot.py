"""Файл запуска бота ScholarshipTracker."""
import asyncio
import logging

from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode, setup_dialogs

from bot.create_bot import bot, dp
from bot.states import Account, Login
from bot.tasks import scheduler
from db import quick_commands as commands
from handlers.account_handler import account
from handlers.find_result_handler import find_result
from handlers.login_handler import login
from handlers.settings_handler import settings
from handlers.top_handler import students_top
from utils.commands import set_commands
from utils.help_functions import delete_old_info
from utils.messages import InfoMessage

# Включаем обработчики команд
dp.include_router(login)
dp.include_router(account)
dp.include_router(students_top)
dp.include_router(find_result)
dp.include_router(settings)

# Настраиваем диалоги
setup_dialogs(dp)


@dp.message(Command("start"))
async def start(message: Message, dialog_manager: DialogManager):
    """Обработчик команды '/start'."""
    # Получаем информацию о чате
    chat_info = await bot.get_chat(message.chat.id)
    # Проверяем, является ли чат супергруппой
    if chat_info.type != 'supergroup':
        # Получаем информацию о пользователе
        activity_info = await commands.get_activity_info(message.from_user.id)
        # Если информация о пользователе не найдена, создаем ее
        if not activity_info:
            activity_info = await commands.start_tracking_info(message.from_user.id)
        # Если диалог уже был запущен, отправляем сообщение
        if activity_info.dialog_was_started:
            await message.reply(InfoMessage.DIALOG_HAS_ALREADY_STARTED_TEXT)
        else:
            # Обновляем информацию о пользователе
            await activity_info.update(dialog_was_started=True).apply()
            # Если это первое сообщение в чате, обновляем информацию о нем
            if not activity_info.first_chat_message_id:
                await activity_info.update(first_chat_message_id=message.message_id).apply()
            # Запускаем диалог
            await dialog_manager.start(Login.START, mode=StartMode.RESET_STACK)


@dp.message(Command("account"))
async def account_menu(message: Message, dialog_manager: DialogManager):
    """Обработчик команды '/account'."""
    # Получаем информацию о чате
    chat_info = await bot.get_chat(message.chat.id)
    # Проверяем, является ли чат супергруппой
    if chat_info.type != 'supergroup':
        # Получаем информацию о пользователе
        activity_info = await commands.get_activity_info(message.from_user.id)
        # Если пользователь еще не авторизован, отправляем сообщение
        if activity_info and not activity_info.is_login:
            await message.reply(InfoMessage.NEED_LOGIN_TEXT)
        else:
            # Запускаем диалог
            await dialog_manager.start(Account.START, mode=StartMode.RESET_STACK)


@dp.message(Command("info"))
async def info(message: Message, dialog_manager: DialogManager):
    """Обработчик команды '/help'."""
    # Получаем информацию о чате
    chat_info = await bot.get_chat(message.chat.id)
    # Проверяем, является ли чат супергруппой
    if chat_info.type != 'supergroup':
        info_text = InfoMessage.INFO_TEXT
        # Отправляем пользователю информацию о проекте
        await message.answer(info_text, parse_mode=ParseMode.HTML)


@dp.message(Command("reset_all"))
async def reset_all(message: Message, dialog_manager: DialogManager):
    """Обработчик команды '/reset_all'."""
    # Получаем информацию о чате
    chat_info = await bot.get_chat(message.chat.id)
    # Проверяем, является ли чат супергруппой
    if chat_info.type != 'supergroup':
        # Получаем информацию о активности пользователя
        activity_info = await commands.get_activity_info(message.from_user.id)

        # Если информация о активности пользователя существует
        if activity_info:
            # Если диалог пользователя был запущен
            if activity_info.dialog_was_started:
                # Отправляем сообщение об успешном сбросе диалога
                await message.answer(InfoMessage.RESET_SUCCESS_TEXT)
                # Обновляем информацию о активности пользователя
                await activity_info.update(dialog_was_started=False, is_login=False).apply()
                # Сбрасываем стек диалога
                await dialog_manager.reset_stack()
                # Удаляем старую информацию о пользователе
                await delete_old_info(message)
        # Если информация о активности пользователя не существует или диалог не
        # был запущен
        elif not activity_info or not activity_info.dialog_was_started:
            # Отправляем сообщение о том, что диалог не был запущен
            await message.reply(InfoMessage.DIALOG_HAS_NO_ALREADY_STARTED_TEXT)


async def main():
    """Функция запуска основных процессов бота."""
    # Запускаем планировщик задач
    scheduler.start()
    # Устанавливаем команды для бота
    await set_commands(bot)
    # Запускаем опрос обновлений для бота
    await dp.start_polling(bot, skip_updates=True)


if __name__ == '__main__':
    # Настраиваем логирование
    file_log = logging.FileHandler("logs/bot_logs.log")
    console_out = logging.StreamHandler()
    logging.basicConfig(
        level=logging.INFO,
        handlers=(file_log, console_out),
        format="%(asctime)s %(levelname)s: %(message)s"
    )
    try:
        # Запуск основных процессов бота
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Работа бота остановлена с клавиатуры!")
