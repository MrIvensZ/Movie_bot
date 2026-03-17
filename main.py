from telebot import TeleBot, apihelper

from config import Config
from database import Database
from models import MoviesORM
from movie_bot import Movie_bot


apihelper.READ_TIMEOUT = 60
apihelper.CONNECT_TIMEOUT = 60


def main():
    db = Database(MoviesORM)
    telebot = TeleBot(Config.TOKEN)
    bot = Movie_bot(telebot=telebot, db=db)
    bot.run()


if __name__ == '__main__':
    main()
