"""
Класс Movie_bot отвечает за функционал telegram-бота
"""

from database import Database
from telebot import TeleBot, types
from tabulate import tabulate

from config import Config
from handlers import ask_for_input


class Movie_bot():
    def __init__(self):
        self.bot = TeleBot(token=Config.TOKEN)
        self.db = Database()
        self._register_handlers()

    def _register_handlers(self):
        self.bot.message_handler(commands=['start'])(self.start)
        self.bot.message_handler(commands=['поиск'])(self.searching)
        self.bot.message_handler(commands=['фильмы'])(self.show_movies)
        self.bot.message_handler(commands=['обновить'])(self.update_title)
        self.bot.message_handler(commands=['удалить'])(self.delete_movie)
        self.bot.message_handler(commands=['добавить'])(self.add_movie)

    def start(self, message):
        chat_id = message.chat.id
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.row(types.KeyboardButton('/фильмы'),)
        keyboard.row(
            types.KeyboardButton('/добавить'),
            types.KeyboardButton('/удалить'),
            types.KeyboardButton('/обновить'),
            types.KeyboardButton('/поиск'),
            )

        self.bot.send_message(
            chat_id,
            text='Опять работа?',
            reply_markup=keyboard,
        )

    def searching(self, message):
        chat_id = message.chat.id
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.row(
            types.KeyboardButton('дата'),
            types.KeyboardButton('название'),)
        self.bot.send_message(chat_id,
                              text='Что вы хотите искать?',
                              reply_markup=keyboard,)
        self.bot.register_next_step_handler(message, self.choice_search)

    def choice_search(self, message):
        chat_id = message.chat.id
        if message.text == 'дата':
            self.bot.send_message(chat_id, 'Введите название.')
            self.bot.register_next_step_handler(message, self.search_date)
        elif message.text == 'название':
            self.bot.send_message(chat_id, 'Введите дату.')
            self.bot.register_next_step_handler(message, self.search_title)

    def search_date(self, message):
        chat_id = message.chat.id
        title = message.text
        date_list = self.db.search_date(title)
        if not date_list:
            self.bot.send_message(chat_id, 'Такого названия нет.')
        else:
            date = date_list[0][0]
            self.bot.send_message(chat_id, f'"{title}" был отсмотрен: {date}')

    def search_title(self, message):
        chat_id = message.chat.id
        date = message.text
        title_list = self.db.search_title(date)
        if not title_list:
            self.bot.send_message(chat_id, 'Такой даты нет.')
        else:
            title = title_list[0][0]
            self.bot.send_message(chat_id, f'{date} был отсмотрен "{title}"')

    def show_movies(self, message):
        chat_id = message.chat.id
        movies = self.db.get_movies()
        table = tabulate(movies, headers=["Название", "Дата"],
                         tablefmt="pretty")
        self.bot.send_message(chat_id, f"<pre>{table}</pre>",
                              parse_mode="HTML")

    def update_title(self, message):
        ask_for_input(
            self.bot, message,
            'Введите название фильма',
            self.update_button
            )

    def update_button(self, message):
        chat_id = message.chat.id
        old_title = message.text
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.row(
            types.KeyboardButton('название'),
            types.KeyboardButton('дата'),)
        self.bot.send_message(
            chat_id,
            text='Какое поле нужно обновить?',
            reply_markup=keyboard,
            )
        self.bot.register_next_step_handler(
            message,
            self.choice_update,
            old_title
            )

    def choice_update(self, message, old_title):
        if message.text == 'название':
            ask_for_input(
                message,
                'Введите новое название.',
                self.new_title,
                old_title
                )
        elif message.text == 'дата':
            ask_for_input(
                self.bot,
                message,
                'Введите новую дату.',
                self.new_date,
                old_title
                )

    def new_title(self, message, old_title):
        chat_id = message.chat.id
        new_title = message.text
        self.db.update_title(title=old_title, new_title=new_title)
        self.bot.send_message(
            chat_id,
            (f'Название фильма {old_title} было изменено на {new_title}.')
            )

    def new_date(self, message, old_title):
        chat_id = message.chat.id
        new_date = message.text
        self.db.update_date(title=old_title, new_date=new_date)
        self.bot.send_message(
            chat_id,
            (f'Дата просмотра фильма {old_title} была изменена на {new_date}.')
            )

    def delete_movie(self, message):
        ask_for_input(
            self.bot,
            message,
            'Введите название фильма',
            self.delete_title
            )

    def delete_title(self, message):
        chat_id = message.chat.id
        title = message.text
        self.db.delete_movie(title=title)
        self.bot.send_message(
            chat_id,
            f'Фильм {title} удалён из базы данных.'
            )

    def add_movie(self, message):
        ask_for_input(
            self.bot,
            message,
            'Введите название фильма.',
            self.save_title
            )

    def save_title(self, message):
        title = message.text
        ask_for_input(
            self.bot,
            message,
            'Введите дату просмотра.',
            self.save_date,
            title
            )

    def save_date(self, message, title):
        date = message.text
        self.db.add_movie(title=title, search_date=date)
        self.bot.send_message(
            message.chat.id,
            (f'Фильм {title} занесён в базу данных.\nДата просмотра: {date}.')
            )

    def run(self):
        print('🤖 Бот запущен. Нажмите Ctrl+C для остановки.')
        self.bot.polling()
