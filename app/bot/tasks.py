"""Таск-менеджер бота."""
from datetime import datetime, timedelta

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from api.google_sheets import update_summary_table
from db.db_gino import on_db_startup

# Создание экземпляра таск-менеджера
scheduler = AsyncIOScheduler()

# Создание триггера для обновления таблицы сводки каждый час
trigger = IntervalTrigger(seconds=60 * 10)
# Добавление задачи на обновление таблицы сводки в таск-менеджере
scheduler.add_job(update_summary_table, trigger)

# Создание даты и времени запуска задачи на инициализацию базы данных
db_run_at = datetime.now() + timedelta(seconds=5)
# Добавление задачи на инициализацию базы данных в таск-менеджере
scheduler.add_job(on_db_startup, 'date', run_date=db_run_at)
