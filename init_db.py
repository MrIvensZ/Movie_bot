"""
Скрипт для инициализации базы данных
Запуск: python init_db.py
"""

import logging
import psycopg2
import sys

from config import Config


def init_database():
    """
    Создание таблицы movies в БД
    """
    conn_params = {
        'host': Config.DB_HOST,
        'user': Config.DB_USER,
        'password': Config.DB_PASSWORD,
        'dbname': Config.DB_NAME,
        'port': Config.DB_PORT
    }

    try:
        with psycopg2.connect(**conn_params) as conn:
            with conn.cursor() as cur:
                cur.execute('''
                            CREATE TABLE IF NOT EXISTS movies
                            (
                            title TEXT NOT NULL,
                            search_date TEXT NOT NULL
                            )
                            ''')
                cur.execute('''
                            SELECT EXISTS
                            (SELECT FROM information_schema.tables
                            WHERE table_name = 'movies')
                            ''')
                table_exist = cur.fetchone()[0]
                if table_exist:
                    print('✅ Таблица "movies" успешно создана')
                    return True

    except Exception as e:
        logging.error(f"Ошибка при подключении к БД: {e}")


if __name__ == '__main__':
    print('🔄 Инициализация базы данных...')
    if init_database():
        print('\n🎉 База данных готова к работе!')
        sys.exit(0)
    else:
        print('\n💥 Ошибка инициализации базы данных')
        sys.exit(1)
