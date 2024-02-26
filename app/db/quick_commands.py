"""Команды для упрощенного доступа к базы данных из кода."""
from asyncpg import UniqueViolationError

from .schemas.info import ActivityInformation


async def get_activity_info(user_telegram_id):
    """Получить информацию активности по id из telegram."""
    # Используем метод query для получения информации о активности пользователя
    # Если активность не найдена, метод gino.first() вернет None
    activity_info = await ActivityInformation.query.where(ActivityInformation.user_telegram_id == user_telegram_id).gino.first()
    return activity_info


async def start_tracking_info(user_telegram_id: int, **kwargs):
    """Начать отслеживание активности."""
    try:
        # Создаем экземпляр класса ActivityInformation с указанными параметрами
        activity_info = ActivityInformation(
            user_telegram_id=user_telegram_id,
            dialog_was_started=False,
            is_login=False,
            first_chat_message_id=None
        )
        # Сохраняем информацию о активности в базе данных
        await activity_info.create()
        return activity_info
    except UniqueViolationError:
        # Если активность уже ведется, выводим сообщение об ошибке
        print('Активность уже ведется!')
