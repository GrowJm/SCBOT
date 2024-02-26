"""Основные модели для БД."""
from sqlalchemy import BigInteger, Boolean, Column, sql

from ..db_gino import TimedBaseModel


class ActivityInformation(TimedBaseModel):
    """Модель активности пользователя."""
    __tablename__ = "activity_info"
    # Идентификатор активности пользователя
    id = Column(BigInteger, unique=True, nullable=False, primary_key=True)
    # Идентификатор пользователя в Телеграме
    user_telegram_id = Column(BigInteger, unique=True, nullable=False)
    # Флаг, указывающий на то, что диалог с пользователем был начат
    dialog_was_started = Column(Boolean)
    # Флаг, указывающий на то, что пользователь авторизован
    is_login = Column(Boolean)
    # Идентификатор студента
    student_id = Column(BigInteger, unique=True)
    # Идентификатор первого сообщения пользователя в чате
    first_chat_message_id = Column(BigInteger, nullable=True)
    # Запрос для получения активности пользователя
    query: sql.select

    def __str__(self) -> str:
        return f"Активность пользователя: {self.user_telegram_id}"
