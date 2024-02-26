"""Функции-обработчики для вывода общих результатов."""
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const, Jinja

from bot.states import BestStudent
from getters.account_getter import get_account_data
from utils.messages import ButtonMessage

from .basic_handler import close_subdialog

# Создаем диалог для вывода топа студентов
students_top = Dialog(
    # Определяем окно диалога лучших студентов
    Window(
        # Определяем виджет для вывода результатов
        Jinja(
            # Шаблон для вывода результатов
            "<pre>{{top5_table_text}}</pre>"
        ),
        # Определяем кнопку для возврата на предыдущий экран
        Button(
            # Текст кнопки
            Const(ButtonMessage.GO_BACK_BUTTON_TEXT),
            # Идентификатор кнопки
            id="close_top",
            # Обработчик нажатия на кнопку
            on_click=close_subdialog,
        ),
        # Состояние диалога
        state=BestStudent.START,
        # Функция для получения данных
        getter=get_account_data
    ),
)
