import psycopg2
import logging

from config import Config


class Database():
    """
    Класс БД
    """
    def __init__(self):
        self.database_parametres = {
            'host': Config.DB_HOST,
            'user': Config.DB_USER,
            'password': Config.DB_PASSWORD,
            'dbname': Config.DB_NAME,
            'port': Config.DB_PORT
            }
        self.start_database()  # при инициализации объекта класса, создаётся таблица в БД

    def start_database(cls):
        """
        Создание таблицы с фильмами

        :param cls: Database class
        """
        try:
            with psycopg2.connect(**cls.DATABASE_PARAMETRES) as conn:
                with conn.cursor() as cur:
                    cur.execute('''
                                CREATE TABLE IF NOT EXISTS movies
                                (
                                title TEXT NOT NULL,
                                search_date TEXT NOT NULL
                                )
                                ''')
        except Exception as e:
            logging.error(f"Ошибка при подключении к БД: {e}")

    def db_add_movie(cls, title: str, search_date: str):
        """
        Добавление фильма в БД

        :param cls: Database class
        :param title: название фильма
        :type title: str
        :param search_date: дата просмотра фильма
        :type search_date: str
        """
        try:
            with psycopg2.connect(**cls.DATABASE_PARAMETRES) as conn:
                with conn.cursor() as cur:
                    cur.execute('''
                                INSERT INTO movies
                                (title, search_date)
                                VALUES (%s,%s)''',
                                (title, search_date)
                                )
                    conn.commit()
        except Exception as e:
            logging.error(f"Ошибка при добавлении фильма: {e}")

    def db_delete_movie(cls, title: str):
        """
        Удаление фильма из таблицы

        :param cls: Database class
        :param title: название фильма
        :type title: str
        """
        try:
            with psycopg2.connect(**cls.DATABASE_PARAMETRES) as conn:
                with conn.cursor() as cur:
                    cur.execute('''
                                DELETE FROM movies
                                WHERE title = %s''',
                                (title,)
                                )
                conn.commit()
        except Exception as e:
            logging.error(f"Ошибка при удалении фильма: {e}")

    def db_update_title(cls, title: str, new_title: str):
        """
        Обновление названия фильма

        :param cls: Database class
        :param title: старое название фильма
        :type title: str
        :param new_title: новое название
        :type new_title: str
        """
        try:
            with psycopg2.connect(**cls.DATABASE_PARAMETRES) as conn:
                with conn.cursor() as cur:
                    cur.execute('''
                                UPDATE movies
                                SET title = %s
                                WHERE title = %s
                                ''',
                                (new_title, title)
                                )
                conn.commit()
        except Exception as e:
            logging.error(f"Ошибка при обновлении названия фильма: {e}")

    def db_update_date(cls, title: str, new_date: str):
        """
        Обновление даты просмотра фильма

        :param cls: Database class
        :param title: название фильма
        :type title: str
        :param new_date:новая дата просмотра
        :type new_date: str
        """
        try:
            with psycopg2.connect(**cls.DATABASE_PARAMETRES) as conn:
                with conn.cursor() as cur:
                    cur.execute('''
                                UPDATE movies
                                SET search_date = %s
                                WHERE title = %s
                                ''',
                                (new_date, title)
                                )
                conn.commit()
        except Exception as e:
            logging.error(f"Ошибка при обновлении даты просмотра фильма: {e}")
