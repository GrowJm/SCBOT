"""Базовые модели для БД."""
import datetime
from typing import List

import sqlalchemy as sa
from gino import Gino

from bot.settings import POSTGRES_URI

# Инициализация движка базы данных
db = Gino()


class BaseModel(db.Model):
    """Базовая модель для БД."""
    __abstract__ = True

    def __str__(self):
        model = self.__class__.__name__
        table: sa.Table = sa.inspect(self.__class__)
        primary_key_columns: List[sa.Column] = table.primary_key.columns
        values = {
            column.name: getattr(self, self._column_name_map[column.name])
            for column in primary_key_columns
        }
        values_str = " ".join(
            f"{name}={value!r}" for name,
            value in values.items())
        return f"<{model} {values_str}>"


class TimedBaseModel(BaseModel):
    """Базовая модель с трекером даты создания и изменения для БД."""
    __abstract__ = True

    created_at = db.Column(db.DateTime(True), server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime(True),
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
        server_default=db.func.now(),
    )


async def on_db_startup():
    """Запуск БД при старте бота."""
    print("Установка связи с PostgreSQL")
    # Установить соединение с базой данных
    await db.set_bind(POSTGRES_URI)
    # Когда нужно удалить базу при старте проекта
    #await db.gino.drop_all()
    await db.gino.create_all()
