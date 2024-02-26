"""Сообщения бота."""


class InfoMessage:
    """Информационные сообщения бота."""
    DIALOG_HAS_ALREADY_STARTED_TEXT = (
        'Вы уже начали работу с ботом!\n'
        'Если хотите начать сначала выполните команду сброса /reset_all.'
    )
    DIALOG_HAS_NO_ALREADY_STARTED_TEXT = (
        'Вы еще не начали общение с ботом. Пора начать!\n'
        'Если хотите начать выполните команду сброса /start.'
    )
    NEED_LOGIN_TEXT = (
        'Прежде чем использовать данную команду, пожалуйста, выполните вход.'
    )
    RESET_SUCCESS_TEXT = (
        'Сброс успешно произведен!'
    )

    START_TEXT = (
        'Здравствуйте! Для того, что начать работу с ботом - выполните вход.\n'
    )
    INFO_TEXT = (
        'Привет! Я - ваш дружелюбный бот, созданный для помощи студентам в определении их положения в рейтинговой таблице. '
        'Моя основная задача - анализировать данные из трех таблиц: <b>Успеваемость</b>, <b>Посещаемость</b> и <b>Грамоты</b>. \n\n'

        'Вот как я работаю:\n'
        '1. <b>Успеваемость</b>: Я анализирую оценки студентов по 100-балльной шкале.\n'
        '2. <b>Посещаемость</b>: Я также учитываю посещаемость студентов, также оценивая ее по 100-балльной шкале.\n'
        '3. <b>Грамоты</b>: Я подсчитываю количество грамот, полученных студентом.\n\n'

        'На основе этих данных, я формирую общий рейтинг каждого студента. Чем выше средний балл по этим трем категориям, '
        'тем выше шанс студента получить стипендию. Вот как я оцениваю шансы:\n'
        '- Если средний балл <b>меньше 75</b>, то шанс получить стипендию <b>низкий</b>.\n'
        '- Если средний балл <b>от 75 до 85</b>, то шанс <b>высокий</b>.\n'
        '- Если средний балл <b>больше 85</b>, то шанс <b>очень высокий</b>.\n\n'

        'Все, что вам нужно сделать, это войти в вашу учетную запись, и я предоставлю вам всю необходимую информацию.\n'
        'Надеюсь, я смогу помочь вам в вашем образовательном пути! 😊'
    )
    NEED_USERNAME_TEXT = (
        'Введите имя пользователя'
    )
    NEED_PASSWORD_TEXT = (
        'Введите пароль'
    )
    PROFILE_TEXT = (
        'Ваш профиль ☕️'
    )
    NEED_STUDENT_ID_TEXT = (
        'Введите id студента'
    )
    INVALID_ID_TEXT = (
        'id должнен быть числом'
    )
    INVALID_USERNAME_TEXT = (
        'Логин не может содержать более одного набора символов'
    )
    INVALID_PASSWORD_TEXT = (
        'Пароль не может содержать более одного набора символов'
    )
    WRONG_AUTH_TEXT = (
        'Данные неверны. Попробуйте еще раз!'
    )
    SUCCESS_AUTH_TEXT = (
        'Вход выполнен успешно!'

    )
    SUCCESS_LOGOUT_TEXT = (
        'Выход выполнен успешно!'
    )


class ButtonMessage:
    """Тексты кнопок бота."""
    LOGIN_BUTTON_TEXT = (
        'Войти'
    )
    BEST_STUDENT_BUTTON_TEXT = (
        'Показать ТОП студентов 🔝'
    )
    FIND_RESULT_BUTTON_TEXT = (
        'Найти результаты 🔎'
    )
    SETTINGS_BUTTON_TEXT = (
        'Настройки ⚙️'
    )
    LOGOUT_BUTTON_TEXT = (
        'Выйти из учетной записи'
    )
    GO_BACK_BUTTON_TEXT = (
        'Назад ↩️'
    )