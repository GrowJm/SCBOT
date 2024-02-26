"""Функции-обработчики для личного кабинета."""
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button, Row
from aiogram_dialog.widgets.text import Const, Jinja

from bot.states import Account
from handlers.basic_handler import sub_dialog_starter
from utils.messages import ButtonMessage, InfoMessage

# Создаем диалог для личного кабинета
account = Dialog(
    # Определяем окно диалога личного кабинета
    Window(
        # Отображаем информационное сообщение о профиле пользователя
        Jinja(f"<b>{InfoMessage.PROFILE_TEXT}</b>"),
        # Кнопка для перехода в диалог лучшего студента
        Button(
            Const(ButtonMessage.BEST_STUDENT_BUTTON_TEXT),
            id="BestStudent",
            on_click=sub_dialog_starter),
        # Кнопка для перехода в диалог поиска результатов
        Button(
            Const(ButtonMessage.FIND_RESULT_BUTTON_TEXT),
            id="FindResult",
            on_click=sub_dialog_starter),
        # Отображаем кнопки настроек
        Row(
            Button(
                Const(ButtonMessage.SETTINGS_BUTTON_TEXT),
                id="Settings",
                on_click=sub_dialog_starter),
        ),
        # Устанавливаем начальное состояние диалога
        state=Account.START,
    ),
)
