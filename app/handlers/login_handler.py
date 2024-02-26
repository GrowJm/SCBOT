"""Функции-обработчики для входа."""
from aiogram.types import ContentType, Message
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Const

from api.google_sheets import check_student_credentials
from bot.states import Account, Login
from db import quick_commands as commands
from getters.login_getter import get_login_data
from utils.help_functions import delete_old_info
from utils.messages import ButtonMessage, InfoMessage
from utils.validators import one_word_validator

from .basic_handler import go_next


async def process_username(message: Message, dialog: Dialog, dialog_manager: DialogManager):
    """Функция-обработчик поля логина."""
    username = message.text
    data = dialog_manager.dialog_data

    # Проверяем валидность логина (должен быть одним словом)
    if not one_word_validator(username):
        await message.reply(InfoMessage.INVALID_USERNAME_TEXT)
    else:
        # Сохраняем логин в данных диалога
        data['username'] = username
        # Удаляем старые данные пользователя
        await delete_old_info(message)
        # Переходим к следующему полю
        await dialog_manager.next()


async def process_password(message: Message, dialog: Dialog, dialog_manager: DialogManager):
    """Функция-обработчик поля пароля."""
    password = message.text
    data = dialog_manager.dialog_data
    user_telegram_id = dialog_manager.event.from_user.id
    # Получаем данные о пользователе по id
    activity_info = await commands.get_activity_info(user_telegram_id)

    # Проверяем валидность пароля (должен быть одним словом)
    if not one_word_validator(password):
        await message.reply(InfoMessage.INVALID_PASSWORD_TEXT)
    else:
        # Сохраняем пароль в данных диалога
        data['password'] = password
        # Проверяем учетные данные пользователя
        student_id = check_student_credentials(**data)
        if student_id:
            # Обновляем информацию о пользователе
            await activity_info.update(is_login=True, student_id=student_id).apply()
            # Удаляем старые данные пользователя
            await delete_old_info(message)
            # Отправляем стикер с изображением успешного входа
            await message.answer_sticker(r'CAACAgIAAxkBAAEBYURlJRMZEaQl2Yu2WtJt_-k0plYaNwAC_gADVp29CtoEYTAu-df_MAQ')
            # Отправляем сообщение об успешном входе
            await message.answer(InfoMessage.SUCCESS_AUTH_TEXT)
            # Запускаем диалог аккаунта
            await dialog_manager.start(Account.START, data=data)
        else:
            # Отправляем стикер с изображением ошибки
            await message.answer_sticker(r'CAACAgIAAxkBAAEDuFhl2lXxjT5O_McMbfrRN-RD8_ql6gACIwoAAm4y2AABPSVjIop2ifc0BA')
            # Отправляем сообщение об ошибке
            await message.answer(InfoMessage.WRONG_AUTH_TEXT)
            # Возвращаемся к полю логина
            await dialog_manager.switch_to(Login.username)


# Окно входа
login = Dialog(
    # Окно стартового изображения и текста
    Window(
        DynamicMedia("start_image"),
        Const(
            InfoMessage.START_TEXT,
        ),
        # Кнопка входа
        Button(
            Const(
                ButtonMessage.LOGIN_BUTTON_TEXT),
            id="login",
            on_click=go_next),
        state=Login.START
    ),
    # Окно ввода логина
    Window(
        Const(
            InfoMessage.NEED_USERNAME_TEXT,
        ),
        # Поле ввода логина
        MessageInput(process_username, content_types=ContentType.TEXT),
        state=Login.username
    ),
    # Окно ввода пароля
    Window(
        Const(
            InfoMessage.NEED_PASSWORD_TEXT,
        ),
        # Поле ввода пароля
        MessageInput(process_password, content_types=ContentType.TEXT),
        state=Login.password
    ),
    # Метод получения данных для входа
    getter=get_login_data
)
