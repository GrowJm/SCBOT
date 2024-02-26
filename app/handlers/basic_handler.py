"""Базовые функции-обработчики."""
import sys
from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from bot.states import *


async def go_back(callback: CallbackQuery, button: Button,
                  dialog_manager: DialogManager):
    """Функция отката диалога."""
    # Переход на предыдущий шаг диалога
    await dialog_manager.back()


async def go_next(callback: CallbackQuery, button: Button,
                  dialog_manager: DialogManager):
    """Функция продолжения диалога."""
    # Переход на следующий шаг диалога
    await dialog_manager.next()


def str_to_class(classname):
    """Функция получения класса из строчного названия."""
    # Получение класса из модуля, где он определен
    return getattr(sys.modules[__name__], classname)


async def sub_dialog_starter(callback: CallbackQuery, widget: Any,
                             dialog_manager: DialogManager):
    """Функция старта поддиалога."""
    # Получение данных текущего диалога
    data = dialog_manager.dialog_data
    # Получение класса поддиалога из строчного названия
    sub_dialog = str_to_class(callback.data)
    # Запуск поддиалога с передачей данных
    await dialog_manager.start(sub_dialog.START, data=data)


async def close_subdialog(callback: CallbackQuery, button: Button,
                          dialog_manager: DialogManager):
    """Функция завершения поддиалога."""
    # Завершение поддиалога
    await dialog_manager.done()
