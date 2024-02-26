"""Данные работы с личным кабинетом."""
from aiogram_dialog import DialogManager
from prettytable import PrettyTable

from api.google_sheets import sh
from db import quick_commands as commands


async def show_table(student_id, is_search=True):
    """Формирование таблицы."""
    # Получение данных из листа "Общий рейтинг"
    worksheet = sh.worksheet("Общий рейтинг")
    records = worksheet.get_all_records()

    # Поиск позиции студента в рейтинге
    if student_id:
        student_id = int(student_id)
    current_student_position = next((i for i, record in enumerate(
        records) if record['student_id'] == student_id), None)

    # Создание таблицы
    table = PrettyTable()
    table.field_names = ["Позиция", "ID", "Балл", "Вероятность"]

    # Заполнение таблицы данными при поиске по student_id
    if is_search:
        # Если студент найден
        if current_student_position is not None:
            student_id_record = records[current_student_position]
            table.add_row([current_student_position + 1,
                           student_id_record['student_id'],
                           "{:.3f}".format(
                               student_id_record['overall_average']),
                           student_id_record['scholarship_chance']])
        # Если студент не найден
        else:
            table.add_row(["x", student_id, "x", "x"])
    # Заполнение таблицы данными о топ-5 студентах
    else:
        for i, record in enumerate(records[:5]):
            if int(record['student_id']) == student_id:
                # Добавление маркер текущего пользователя
                marker = '(Вы){position}(Вы)'
            else:
                marker = '{position}'
            table.add_row([marker.format(position=str(i + 1)),
                           record['student_id'],
                           "{:.3f}".format(record['overall_average']),
                           record['scholarship_chance']])

        # Если студент находится в топ-5
        if current_student_position is not None and current_student_position >= 5:
            student_id_record = records[current_student_position]
            table.add_row([str(current_student_position + 1),
                           student_id_record['student_id'],
                           "{:.3f}".format(
                student_id_record['overall_average']),
                student_id_record['scholarship_chance']])

    # Выравнивание столбцов по центру
    table.align = "c"

    # Возврат таблицы
    return table


async def get_account_data(dialog_manager: DialogManager, **kwargs):
    """Данные для диалога, связанного с личным кабинетом."""
    # Получение идентификатора пользователя
    user_telegram_id = dialog_manager.event.from_user.id
    # Получение информации о студенте
    activity_info = await commands.get_activity_info(user_telegram_id)
    # Формирование таблицы с топ-5 студентами
    top5_table_text = await show_table(activity_info.student_id, is_search=False)

    # Получение данных для поиска студента
    data = dialog_manager.dialog_data
    search_student_id = data.get('search_student_id', None)
    # Формирование таблицы с информацией о студенте
    student_id_table_text = await show_table(search_student_id, is_search=True)

    # Возврат данных для диалога
    return {
        "top5_table_text": top5_table_text,
        "student_id_table_text": student_id_table_text
    }
