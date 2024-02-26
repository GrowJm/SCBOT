"""Валидаторы данных от пользователя."""


def one_word_validator(data):
    """Первичная проверка на количество слов."""
    # Проверяем, есть ли в строке пробелы
    # Если есть, то это означает, что введено несколько слов
    if len(data.split()) != 1:
        return False
    return True
