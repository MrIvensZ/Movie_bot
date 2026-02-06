"""
Класс Movie_bot отвечает за функционал telegram-бота
"""

import logging

from telebot import TeleBot, types
from tabulate import tabulate

from config import Config
from database import Database
from handlers import ask_for_input

bot = TeleBot(token=Config.TOKEN)

class Movie_bot(TeleBot):
    pass