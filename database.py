"""
Класс Database отвечает за взаимодействия с БД
"""

import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import DB_PARAMS, get_url


class Database():
    """
    Класс БД
    """
    def __init__(self, movies_table):
        self.url = get_url(DB_PARAMS)
        self.engine = create_engine(self.url, echo=True)
        self.session = sessionmaker(self.engine)
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
            with self.session() as sess:
                movie = self.movies(title=title, search_date=search_date)
                sess.add(movie)
                sess.commit()
                if sess.get(self.movies, title) is not None:
                    logging.info(f"Фильм '{title}' успешно добавлен")
                    return True
                return False

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
            with self.session() as sess:
                movie = sess.get(self.movies, title)
                sess.delete(movie)
                sess.commit()
                if sess.get(self.movies, title) is None:
                    logging.info(f"Фильм '{title}' успешно удалён")
                    return True
                return False
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
            with self.session() as sess:
                movie = sess.get(self.movies, title)
                movie.title = new_title
                sess.commit()
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
            with self.session() as sess:
                movie = sess.get(self.movies, title)
                movie.search_date = new_date
                sess.commit()
                logging.info(
                    f"Дата просмтора фильма '{title}' изменена на {new_date}"
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
            with self.session() as sess:
                result = sess.query(self.movies).all()
                return result
        except Exception as e:
            logging.error(f'Ошибка при выводе списка фильмов: {e}')
            return []

    def search_date(self, title: str):
        """
        Поиск даты просмотра фильма

        :param title: название фильма
        :type title: str
        """
        try:
            with self.session() as sess:
                movie = sess.get(self.movies, title)
                return movie.search_date
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
            with self.session() as sess:
                movies = (
                    sess
                    .query(self.movies)
                    .filter(self.movies.search_date == date)
                    .all()
                    )
                return movies[0].title
        except Exception as e:
            logging.error(f'Ошибка при поиске названия фильма: {e}')
            return False
