from telebot import TeleBot

from config import Config
from database import Database
from models import movies
from movie_bot import Movie_bot


def main():
    db = Database(movies)
    telebot = TeleBot(Config.TOKEN)
    bot = Movie_bot(telebot=telebot, db=db)
    bot.run()


if __name__ == '__main__':
    main()
