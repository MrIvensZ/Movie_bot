"""
Класс Database отвечает за взаимодействия с БД
"""

import logging

from contextlib import contextmanager
from sqlalchemy import create_engine, insert
from sqlalchemy.engine import URL

from config import Config, DB_PARAMS, get_url
from models import movies


class Database():
    """
    Класс БД
    """
    def __init__(self):
        self.url = get_url(DB_PARAMS)
        self.engine = create_engine(self.url, echo=True)

    # def connect(self):
    #     """
    #     Метод создания соединения с БД
    #     """
    #     if self.engine is None:
    #         try:
    #             self.engine = create_engine(self.url, echo=True)
    #         except Exception as e:
    #             logging.error(f'Ошибка при установке соединения с БД: {e}')
    #     return self.connection

    # def close(self):
    #     """
    #     Метод закрытия соединения

    #     :param conn: объект соединения
    #     """
    #     if self.connection is not None:
    #         self.connection.close()
    #         self.connection = None

    def add_movie(self, title: str, search_date: str):
        """
        Добавление фильма в таблицу

        :param title: название фильма
        :type title: str
        :param search_date: дата просмотра
        :type search_date: str
        """
        try:
            with self.engine.begin() as conn:
                stmt = movies.insert().values(
                    title=title,
                    search_date=search_date
                )
                conn.execute(stmt)
                logging.info(f"Фильм '{title}' успешно добавлен")
                return True
        except Exception as e:
            logging.error(f'Ошибка при добавлении фильма: {e}')
            return False

    def delete_movie(self, title: str):
        """
        Удаление фильма

        :param title: название фильма
        :type title: str
        """
        try:
            with self.get_cursor() as cur:
                cur.execute('''
                            DELETE FROM movies
                            WHERE title = %s''',
                            (title,)
                            )
        except Exception as e:
            logging.error(f'Ошибка при удалении фильма: {e}')

    def update_title(self, title: str, new_title: str):
        """
        Замена названия фильма

        :param title: старое название
        :type title: str
        :param new_title: новое название
        :type new_title: str
        """
        try:
            with self.get_cursor() as cur:
                cur.execute('''
                            UPDATE movies
                            SET title = %s
                            WHERE title = %s
                            ''',
                            (new_title, title)
                            )
        except Exception as e:
            logging.error(f'Ошибка при обновлении названия фильма: {e}')

    def update_date(self, title: str, new_date: str):
        """
        Обновление даты

        :param title: название фильма
        :type title: str
        :param new_date: новая дата
        :type new_date: str
        """
        try:
            with self.get_cursor() as cur:
                cur.execute('''
                            UPDATE movies
                            SET search_date = %s
                            WHERE title = %s
                            ''',
                            (new_date, title)
                            )
        except Exception as e:
            logging.error(
                f'Ошибка при обновлении даты просмотра фильма: {e}')

    def get_movies(self):
        """
        Получение списка фильмов
        """
        try:
            with self.get_cursor() as cur:
                cur.execute('SELECT title, search_date FROM movies;')
                movies = cur.fetchall()
                return movies
        except Exception as e:
            logging.error(f'Ошибка при выводе списка фильмов: {e}')

    def search_date(self, title: str):
        """
        Поиск даты просмотра фильма

        :param title: название фильма
        :type title: str
        """
        try:
            with self.get_cursor() as cur:
                cur.execute('''
                            SELECT search_date
                            FROM movies
                            WHERE title = %s;
                            ''',
                            (title,)
                            )
                date_list = cur.fetchall()
                return date_list
        except Exception as e:
            logging.error(f'Ошибка при поиске даты фильма: {e}')

    def search_title(self, date: str):
        """
        Поиск фильма по дате

        :param date: дата
        :type date: str
        """
        try:
            with self.get_cursor() as cur:
                cur.execute('''
                            SELECT title
                            FROM movies
                            WHERE search_date = %s;
                            ''',
                            (date,)
                            )
                title_list = cur.fetchall()
                return title_list
        except Exception as e:
            logging.error(f'Ошибка при поиске названия фильма: {e}')

    def __del__(self):
        self.close()
