"""Вспомогательные функции проекта."""
from bot.create_bot import bot
from db.quick_commands import get_activity_info


async def delete_old_info(message):
    """Удаление старых сообщений от бота."""
    # Получение информации о активности пользователя из базы данных
    activity_info = await get_activity_info(message.from_user.id)
    # Получение идентификатора первого сообщения в чате
    first_chat_message_id = activity_info.first_chat_message_id
    # Обновление информации о активности пользователя в базе данных
    await activity_info.update(first_chat_message_id=message.message_id).apply()
    # Удаление старых сообщений от бота
    for i in range(message.message_id - 1, first_chat_message_id - 1, -1):
        try:
            # Удаление сообщения с идентификатором i
            await bot.delete_message(message.from_user.id, i)
        except Exception:
            # Вывод сообщения об ошибке, если сообщение с данным
            # идентификатором невозможно удалить
            print(f'Сообщение с данным id невозможно удалить: {i}')
