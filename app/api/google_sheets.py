"""Работа с таблицами google spreadsheets."""
import gspread
from gspread import service_account

# Авторизация и открытие таблицы Google Sheets
gc = service_account(filename='api/credentials.json')
sh = gc.open('sch_tracker')


def check_student_credentials(username, password):
    """Проверка данных при аутентификации."""
    worksheet = sh.worksheet(
        "Аутентификация")  # Выбор worksheet аутентификации
    user_data = worksheet.get_all_records()  # Получение всех записей из worksheet

    for user in user_data:  # Перебор всех записей
        if user['username'] == username and user['password'] == password:
            # Возврат id студента, если данные совпадают
            return user['student_id']

    return None  # Возврат None, если нет совпадений


def get_student_row(worksheet, student_id):
    """Получение позиции студента по id в worksheet."""
    records = worksheet.get_all_records()  # Получение всех записей из worksheet

    for i, record in enumerate(records):  # Перебор всех записей
        if record['student_id'] == student_id:
            # Возврат позиции, если id студента совпадает (+2 из-за
            # особенностей таблицы)
            return i + 2
    return None  # Возврат None, если нет совпадений


def get_all_student_ids():
    """Получение списка всех id студентов."""
    worksheet = sh.worksheet(
        "Аутентификация")  # Выбор worksheet аутентификации
    all_records = worksheet.get_all_records()  # Получение всех записей из worksheet
    all_student_ids = [record['student_id']
                       for record in all_records]  # Получение всех id студентов

    return all_student_ids  # Возврат списка id студентов


def calculate_grade_average_score(student_id):
    """Вычисление среднего балла за все работы студента."""
    worksheet = sh.worksheet("Успеваемость")  # Выбор worksheet успеваемости
    records = worksheet.get_all_records()  # Получение всех записей из worksheet

    # Фильтрация записей по id студента
    student_records = [
        record for record in records if record['student_id'] == student_id]

    if not student_records:  # Если нет записей для студента
        return 0  # Возврат 0

    total_score = sum(record['score']
                      for record in student_records)  # Подсчет общего балла
    # Вычисление среднего балла
    average_score = total_score / len(student_records)

    return average_score  # Возврат среднего балла


def calculate_visiting_average_score(student_id):
    """Вычисление среднего балла за все посещения студента."""
    worksheet = sh.worksheet("Посещаемость")  # Выбор worksheet посещаемости
    records = worksheet.get_all_records()  # Получение всех записей из worksheet

    # Фильтрация записей по id студента
    student_records = [
        record for record in records if record['student_id'] == student_id]

    if not student_records:  # Если нет записей для студента
        return 0  # Возврат 0

    subjects = [subject for subject in student_records[0].keys(
    ) if subject not in ['student_id']]  # Получение списка предметов

    total_attendance = 0  # Инициализация общего количества посещений
    for subject in subjects:
        total_attendance += sum(float(record[subject].split('/')[0]) / float(
            record[subject].split('/')[1]) for record in student_records)

    # Вычисление среднего балла за посещения
    average_attendance = (
        total_attendance / (len(student_records) * len(subjects))) * 100

    return average_attendance  # Возврат среднего балла за посещения


def calculate_overall_average(student_id):
    """Вычисление общий балл студента."""
    grade_average = calculate_grade_average_score(
        student_id)  # Вычисление среднего балла
    visiting_average = calculate_visiting_average_score(
        student_id)  # Вычисление среднего балла за посещения

    overall_average = (grade_average + visiting_average) / \
        2  # Вычисление общего балла

    return overall_average  # Возврат общего балла


def update_summary_table():
    """Обновление итоговой таблицы."""
    try:
        # Выбор worksheet итоговой таблицы
        worksheet = sh.worksheet("Общий рейтинг")
    except gspread.exceptions.WorksheetNotFound:
        # Создание worksheet итоговой таблицы, если она отсутствует
        worksheet = sh.add_worksheet(
            title="Общий рейтинг", rows="100", cols="5")

    worksheet.update('A1',
                     [["student_id",
                       "grade_average",
                       "visiting_average",
                       "overall_average",
                       "scholarship_chance"]])  # Обновление заголовка

    student_ids = get_all_student_ids()  # Получение списка всех id студентов

    data = []  # Инициализация списка данных

    for i, student_id in enumerate(
            student_ids, start=2):  # Перебор всех id студентов
        grade_average = calculate_grade_average_score(
            student_id)  # Вычисление среднего балла
        visiting_average = calculate_visiting_average_score(
            student_id)  # Вычисление среднего балла за посещения
        overall_average = calculate_overall_average(
            student_id)  # Вычисление общего балла
        scholarship_chance = "Высокий" if overall_average > 85 else (
            "Средний" if overall_average > 75 else "Низкий")  # Определение шанса на стипендию

        data.append([student_id, str(grade_average), str(visiting_average), str(
            overall_average), scholarship_chance])  # Добавление данных в список

    # Сортировка данных по общему баллу
    data.sort(key=lambda x: x[3], reverse=True)

    # Обновление worksheet итоговой таблицы данными
    worksheet.update('A2', data)
