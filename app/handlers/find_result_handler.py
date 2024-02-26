"""Функции-обработчики для поиска результатов."""
from aiogram.types import ContentType, Message
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const, Jinja

from bot.states import FindResult
from getters.account_getter import get_account_data
from utils.help_functions import delete_old_info
from utils.messages import ButtonMessage, InfoMessage

from .basic_handler import close_subdialog, go_back


async def process_student_id(message: Message, dialog: Dialog, dialog_manager: DialogManager):
    """Функция-обработчик id студента."""
    student_id = message.text
    data = dialog_manager.dialog_data
    try:
        # Преобразование id студента в число
        student_id = int(student_id)
        # Сохранение id студента в данных диалога
        data['search_student_id'] = student_id
        # Удаление старой информации
        await delete_old_info(message)
        # Переход к следующему окну диалога
        await dialog_manager.next()
    except ValueError:
        # Отправка сообщения об ошибке, если id студента не является числом
        await message.reply(InfoMessage.INVALID_ID_TEXT)

# Диалог поиска результатов
find_result = Dialog(
    # Окно ввода id студента
    Window(
        Const(
            InfoMessage.NEED_STUDENT_ID_TEXT,
        ),
        # Кнопка возврата на предыдущее окно диалога
        Button(
            Const(ButtonMessage.GO_BACK_BUTTON_TEXT),
            id="close_search",
            on_click=close_subdialog,
        ),
        # Поле ввода id студента
        MessageInput(process_student_id, content_types=ContentType.TEXT),
        state=FindResult.START
    ),
    # Окно отображения результатов поиска
    Window(
        Jinja(
            "<pre>{{student_id_table_text}}</pre>"
        ),
        # Кнопка возврата на предыдущее окно диалога
        Button(
            Const(ButtonMessage.GO_BACK_BUTTON_TEXT),
            id="close_search_result",
            on_click=go_back,
        ),
        state=FindResult.SHOW,
        # Получение данных студента
        getter=get_account_data,
    ),
)
