"""Функции-обработчики для диалога настроек."""
from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const, Jinja

from bot.create_bot import bot
from bot.states import Settings
from db import quick_commands as commands
from utils.messages import ButtonMessage, InfoMessage

from .basic_handler import close_subdialog


async def process_logout(callback: CallbackQuery, widget: Any,
                         dialog_manager: DialogManager):
    """Функция-обработчик выхода из аккаунта."""
    # Получение идентификатора пользователя Телеграм
    user_telegram_id = dialog_manager.event.from_user.id
    # Получение информации о активности пользователя
    activity_info = await commands.get_activity_info(user_telegram_id)
    # Обновление информации о активности пользователя
    await activity_info.update(is_login=False, dialog_was_started=False).apply()
    # Сброс стека диалога.
    await dialog_manager.reset_stack()
    # Удаление последнего сообщения пользователя
    last_message_id = callback.message.message_id
    await bot.delete_message(user_telegram_id, last_message_id)
    # Отправка сообщения о успешном выходе из аккаунта
    await bot.send_message(user_telegram_id, InfoMessage.SUCCESS_LOGOUT_TEXT)


# Создание диалога настроек
settings = Dialog(
    # Создание окна диалога настроек
    Window(
        # Отображение кнопки настроек
        Jinja(f"<b>{ButtonMessage.SETTINGS_BUTTON_TEXT}</b>"),
        # Кнопка выхода из аккаунта
        Button(
            Const(ButtonMessage.LOGOUT_BUTTON_TEXT),
            id="logout",
            on_click=process_logout),
        # Кнопка возврата на предыдущий экран
        Button(
            Const(ButtonMessage.GO_BACK_BUTTON_TEXT),
            id="close_settings",
            on_click=close_subdialog,
        ),
        # Состояние диалога настроек
        state=Settings.START
    ),
)
