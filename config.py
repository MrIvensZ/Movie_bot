import os

from dotenv import load_dotenv
from sqlalchemy.engine import URL

load_dotenv()


class Config:
    """
    Конфигурационный класс для бота
    """
    TOKEN = os.getenv('TOKEN')  # токен
    DB_HOST = os.getenv('DB_HOST')  # хост
    DB_USER = os.getenv('DB_USER')  # пользователь БД
    DB_PASSWORD = os.getenv('DB_PASSWORD')  # пароль
    DB_NAME = os.getenv('DB_NAME')  # БД
    DB_PORT = os.getenv('DB_PORT')  # порт


# словарь с параметрами для подключения к БД
DB_PARAMS = {
            'driver': 'postgresql+psycopg2',
            'host': Config.DB_HOST,
            'user': Config.DB_USER,
            'password': Config.DB_PASSWORD,
            'dbname': Config.DB_NAME,
            'port': Config.DB_PORT
            }


def get_url(db_params: dict):
    """
    Возвразает URL адрес для подключения через SQLAlcemy

    :param db_params: словарь с параметрами
    :type db_params: dict
    """
    return (
        '{driver}://{user}:{password}@{host}:{port}/{dbname}'
        .format(**db_params)
        )
