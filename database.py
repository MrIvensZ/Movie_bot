"""
Класс Database отвечает за взаимодействия с БД
"""

import logging

from sqlalchemy import create_engine, delete, insert, select, update

from config import DB_PARAMS, get_url


class Database():
    """
    Класс БД
    """
    def __init__(self, movies_table):
        self.url = get_url(DB_PARAMS)
        self.engine = create_engine(self.url, echo=True)
        self.movies = movies_table

    def insert_movie(self, title: str, search_date: str):
        """
        Добавление фильма в таблицу

        :param title: название фильма
        :type title: str
        :param search_date: дата просмотра
        :type search_date: str
        """
        try:
            with self.engine.begin() as conn:
                stmt = (
                    insert(self.movies)
                    .values(title=title, search_date=search_date)
                    )
                result = conn.execute(stmt)
                if result.rowcount > 0:
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
            with self.engine.begin() as conn:
                stmt = delete(self.movies).where(self.movies.c.title == title)
                result = conn.execute(stmt)
                if result.rowcount > 0:
                    logging.info(f"Фильм '{title}' успешно удалён")
                    return True
        except Exception as e:
            logging.error(f'Ошибка при удалении фильма: {e}')
            return False

    def update_title(self, title: str, new_title: str):
        """
        Замена названия фильма

        :param title: старое название
        :type title: str
        :param new_title: новое название
        :type new_title: str
        """
        try:
            with self.engine.begin() as conn:
                stmt = (
                    update(self.movies)
                    .where(self.movies.c.title == title)
                    .values(title=new_title)
                    )
                result = conn.execute(stmt)
                if result.rowcount > 0:
                    logging.info(
                        f"Название фильма '{title}' изменено на {new_title}"
                        )
                    return True
        except Exception as e:
            logging.error(f'Ошибка при обновлении названия фильма: {e}')
            return False

    def update_date(self, title: str, new_date: str):
        """
        Обновление даты

        :param title: название фильма
        :type title: str
        :param new_date: новая дата
        :type new_date: str
        """
        try:
            with self.engine.begin() as conn:
                stmt = (
                    update(self.movies)
                    .where(self.movies.c.title == title)
                    .values(search_date=new_date)
                    )
                result = conn.execute(stmt)
                if result.rowcount > 0:
                    logging.info(
                        f"дата просмтора фильма '{title}' изменена на {new_date}"
                        )
                    return True
        except Exception as e:
            logging.error(
                f'Ошибка при обновлении даты просмотра фильма: {e}')
            return False

    def get_movies(self):
        """
        Получение списка фильмов
        """
        try:
            with self.engine.connect() as conn:
                query = select(self.movies)
                result = conn.execute(query)
                movies_list = result.fetchall()
                return movies_list
        except Exception as e:
            logging.error(f'Ошибка при выводе списка фильмов: {e}')
            return False

    def search_date(self, title: str):
        """
        Поиск даты просмотра фильма

        :param title: название фильма
        :type title: str
        """
        try:
            with self.engine.connect() as conn:
                query = (
                    select(self.movies.c.search_date)
                    .where(self.movies.c.title == title)
                )
                result = conn.execute(query)
                date = result.fetchone()
                return date
        except Exception as e:
            logging.error(f'Ошибка при поиске даты фильма: {e}')
            return False

    def search_title(self, date: str):
        """
        Поиск фильма по дате

        :param date: дата
        :type date: str
        """
        try:
            with self.engine.connect() as conn:
                query = (
                    select(self.movies.c.title)
                    .where(self.movies.c.search_date == date)
                )
                result = conn.execute(query)
                title = result.fetchone()
                return title
        except Exception as e:
            logging.error(f'Ошибка при поиске названия фильма: {e}')
            return False
