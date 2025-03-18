import psycopg2
import logging

from config import Config

connection = psycopg2.connect(
    host=Config.DB_HOST,
    user=Config.DB_USER,
    password=Config.DB_PASSWORD,
    database=Config.DB_NAME,
)


def start_database():
    try:
        with connection.cursor() as cursor:
            cursor.execute('''
                           CREATE TABLE IF NOT EXISTS movies
                           (
                           title TEXT NOT NULL,
                           search_date TEXT NOT NULL
                           )
                           ''')
    except Exception as e:
        logging.error(f"Ошибка при подключении к БД: {e}")


def db_add_movie(title: str, search_date: str):
    try:
        with connection.cursor() as cursor:
            cursor.execute('''
                           INSERT INTO movies
                           (title, search_date)
                           VALUES (%s,%s)''',
                           (title, search_date)
                           )
            connection.commit()
    except Exception as e:
        logging.error(f"Ошибка при добавлении фильма: {e}")


def db_delete_movie(title: str):
    try:
        with connection.cursor() as cursor:
            cursor.execute('''
                           DELETE FROM movies
                           WHERE title = %s''',
                           (title,)
                           )
        connection.commit()
    except Exception as e:
        logging.error(f"Ошибка при удалении фильма: {e}")


def db_update_title(title: str, new_title: str):
    try:
        with connection.cursor() as cursor:
            cursor.execute('''
                           UPDATE movies
                           SET title = %s
                           WHERE title = %s
                           ''',
                           (new_title, title)
                           )
        connection.commit()
    except Exception as e:
        logging.error(f"Ошибка при обновлении названия фильма: {e}")


def db_update_date(title: str, new_date: str):
    try:
        with connection.cursor() as cursor:
            cursor.execute('''
                           UPDATE movies
                           SET search_date = %s
                           WHERE title = %s
                           ''',
                           (new_date, title)
                           )
        connection.commit()
    except Exception as e:
        logging.error(f"Ошибка при обновлении даты просмотра фильма: {e}")
