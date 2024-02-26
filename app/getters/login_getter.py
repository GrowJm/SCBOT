"""Данные для процесса аутентифицкации."""
from aiogram.enums import ContentType
from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import MediaAttachment

# Функция для получения данных для диалога, связанного со входом


async def get_login_data(dialog_manager: DialogManager, **kwargs):
    """Функция для получения данных для диалога, связанного со входом."""

    # Создаем объект MediaAttachment для изображения, которое будет
    # использоваться в качестве заставки для диалога
    start_image = MediaAttachment(
        ContentType.PHOTO,
        path='media/admin/hello_pic.png'
    )

    # Возвращаем словарь с данными для диалога, связанного со входом
    return {
        "start_image": start_image
    }
