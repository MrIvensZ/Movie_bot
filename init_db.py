"""
Скрипт для инициализации базы данных
Запуск: python init_db.py
"""

import logging
import sys

from sqlalchemy import create_engine, inspect

from config import DB_PARAMS, get_url
from models import Base


def init_database(db_params, declarative_class):
    """
    Создание таблицы movies в БД
    """
    engine = create_engine(get_url(db_params), echo=True)

    try:
        declarative_class.metadata.create_all(engine)
        inspector = inspect(engine)
        if inspector.has_table('movies_orm'):
            print('✅ Таблица "movies" успешно создана')
            return True
        else:
            return False
    except Exception as e:
        logging.error(f"Ошибка при подключении к БД: {e}")


if __name__ == '__main__':
    print('🔄 Инициализация базы данных...')
    if init_database(DB_PARAMS, Base):
        print('\n🎉 База данных готова к работе!')
        sys.exit(0)
    else:
        print('\n💥 Ошибка инициализации базы данных')
        sys.exit(1)
