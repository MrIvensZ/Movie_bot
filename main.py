import logging

from telebot import TeleBot, types

from config import Config
from database import (connection,
                      start_database,
                      db_add_movie,
                      db_delete_movie,
                      db_update_date,
                      db_update_title)
from handlers import ask_for_input

bot = TeleBot(token=Config.TOKEN)


@bot.message_handler(commands=['start',])
def start(message):
    chat_id = message.chat.id
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(types.KeyboardButton('/фильмы'),)
    keyboard.row(
        types.KeyboardButton('/добавить'),
        types.KeyboardButton('/удалить'),
        types.KeyboardButton('/обновить'),
        types.KeyboardButton('/поиск'),
        )

    bot.send_message(
        chat_id,
        text='Опять работа?',
        reply_markup=keyboard,
    )


@bot.message_handler(commands=['поиск',])
def searching(message):
    chat_id = message.chat.id
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(
        types.KeyboardButton('дата'),
        types.KeyboardButton('название'),)
    bot.send_message(chat_id,
                     text='Что вы хотите искать?',
                     reply_markup=keyboard,)
    bot.register_next_step_handler(message, choice_search)


def choice_search(message):
    chat_id = message.chat.id
    if message.text == 'дата':
        bot.send_message(chat_id, 'Введите название.')
        bot.register_next_step_handler(message, search_date)
    elif message.text == 'название':
        bot.send_message(chat_id, 'Введите дату.')
        bot.register_next_step_handler(message, search_title)


def search_date(message):
    chat_id = message.chat.id
    title = message.text
    try:
        with connection.cursor() as cursor:
            cursor.execute('''
                           SELECT search_date
                           FROM movies
                           WHERE title = %s;
                           ''',
                           (title,)
                           )
            date_list = cursor.fetchall()
    except Exception as e:
        logging.error(f"Ошибка при поиске даты фильма: {e}")
    if not date_list:
        bot.send_message(chat_id, 'Такого названия нет.')
    else:
        date = date_list[0][0]
        bot.send_message(chat_id, f'"{title}" был отсмотрен: {date}')


def search_title(message):
    chat_id = message.chat.id
    date = message.text
    try:
        with connection.cursor() as cursor:
            cursor.execute('''
                           SELECT title
                           FROM movies
                           WHERE search_date = %s;
                           ''',
                           (date,)
                           )
            title_list = cursor.fetchall()
    except Exception as e:
        logging.error(f"Ошибка при поиске названия фильма: {e}")
    if not title_list:
        bot.send_message(chat_id, 'Такой даты нет.')
    else:
        title = title_list[0][0]
        bot.send_message(chat_id, f'{date} был отсмотрен "{title}"')


@bot.message_handler(commands=['фильмы',])
def show_movies(message):
    chat_id = message.chat.id
    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT title, search_date FROM movies;')
            movies = cursor.fetchall()
            header = '| Название | Дата |\n|----------|----------|'
            movies_str = [header]
            for movie in movies:
                movies_str.append(f'| {movie[0]} | {movie[1]} |')
    except Exception as e:
        logging.error(f"Ошибка при выводе списка фильмов: {e}")

    bot.send_message(chat_id, '\n'.join(movies_str), parse_mode='Markdown')


@bot.message_handler(commands=['обновить',])
def update_title(message):
    ask_for_input(bot, message, 'Введите название фильма', update_button)


def update_button(message):
    chat_id = message.chat.id
    old_title = message.text
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(
        types.KeyboardButton('название'),
        types.KeyboardButton('дата'),)
    bot.send_message(chat_id,
                     text='Какое поле нужно обновить?',
                     reply_markup=keyboard,)
    bot.register_next_step_handler(message, choice_update, old_title)


def choice_update(message, old_title):
    if message.text == 'название':
        ask_for_input(message, 'Введите новое название.', new_title, old_title)
    elif message.text == 'дата':
        ask_for_input(bot, message, 'Введите новую дату.', new_date, old_title)


def new_title(message, old_title):
    chat_id = message.chat.id
    new_title = message.text
    db_update_title(title=old_title, new_title=new_title)
    bot.send_message(chat_id,
                     (f'Название фильма {old_title}'
                      f' было изменено на {new_title}.')
                     )


def new_date(message, old_title):
    chat_id = message.chat.id
    new_date = message.text
    db_update_date(title=old_title, new_date=new_date)
    bot.send_message(chat_id,
                     (f'Дата просмотра фильма {old_title}'
                      f' была изменена на {new_date}.')
                     )


@bot.message_handler(commands=['удалить',])
def delete_movie(message):
    ask_for_input(bot, message, 'Введите название фильма', delete_title)


def delete_title(message):
    chat_id = message.chat.id
    title = message.text
    db_delete_movie(title=title)
    bot.send_message(chat_id,
                     f'Фильм {title} удалён из базы данных.'
                     )


@bot.message_handler(commands=['добавить',])
def add_movie(message):
    ask_for_input(bot, message, 'Введите название фильма.', save_title)


def save_title(message):
    title = message.text
    ask_for_input(bot, message, 'Введите дату просмотра.', save_date, title)


def save_date(message, title):
    date = message.text
    db_add_movie(title=title, search_date=date)
    bot.send_message(message.chat.id,
                     (f'Фильм {title} занесён в базу данных.'
                      f'\nДата просмотра: {date}.')
                     )


def main():
    start_database()
    bot.polling()


if __name__ == '__main__':
    main()
