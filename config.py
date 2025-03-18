import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    TOKEN = os.getenv('TOKEN')
    DB_HOST = os.getenv('HOST')
    DB_USER = os.getenv('USER')
    DB_PASSWORD = os.getenv('PASSWORD')
    DB_NAME = os.getenv('DATABASE')
