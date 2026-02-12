import os

from dotenv import load_dotenv

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
