import os
import sqlite3

from dotenv import load_dotenv
from telebot import TeleBot, types

load_dotenv()

secret_token = os.getenv('TOKEN')
bot = TeleBot(token=secret_token)

connection = sqlite3.connect('movies_database.db',
                             check_same_thread=False)
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS movies (
id INTEGER PRIMARY KEY,
title TEXT NOT NULL,
search_date TEXT NOT NULL
)
''')


def db_add_movie(title: str, search_date: str):
    cursor.execute('''
                   INSERT INTO movies
                   (title, search_date)
                   VALUES (?, ?)''',
                   (title, search_date)
                   )
    connection.commit()


def db_delete_movie(title: str):
    cursor.execute('''
                   DELETE FROM movies
                   WHERE title = ?''',
                   (title,)
                   )
    connection.commit()


def db_update_title(title: str, new_title: str):
    cursor.execute('''
                   UPDATE movies
                   SET title = ?
                   WHERE title = ?
                   ''',
                   (new_title, title)
                   )
    connection.commit()


def db_update_date(title: str, new_date: str):
    cursor.execute('''
                   UPDATE movies
                   SET search_date = ?
                   WHERE title = ?
                   ''',
                   (new_date, title)
                   )
    connection.commit()


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
    date = cursor.execute('''
                          SELECT search_date
                          FROM movies
                          WHERE title = ?;
                          ''',
                          (title,)
                          )
    date_list = date.fetchall()
    if not date_list:
        bot.send_message(chat_id, 'Такого названия нет.')
    else:
        bot.send_message(chat_id, str(date_list[0]))


def search_title(message):
    chat_id = message.chat.id
    date = message.text
    title = cursor.execute('''
                           SELECT title
                           FROM movies
                           WHERE search_date = ?;
                           ''',
                           (date,)
                           )
    title_list = title.fetchall()
    if not title_list:
        bot.send_message(chat_id, 'Такой даты нет.')
    else:
        bot.send_message(chat_id, str(title_list[0]))


@bot.message_handler(commands=['обновить',])
def update_title(message):
    chat_id = message.chat.id
    bot.send_message(chat_id,
                     'Введите название фильма.')
    bot.register_next_step_handler(message, update_button)


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
    chat_id = message.chat.id
    if message.text == 'название':
        bot.send_message(chat_id, 'Введите новое название.')
        bot.register_next_step_handler(message, new_title, old_title)
    elif message.text == 'дата':
        bot.send_message(chat_id, 'Введите новую дату.')
        bot.register_next_step_handler(message, new_date, old_title)


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
    chat_id = message.chat.id
    bot.send_message(chat_id,
                     'Введите название фильма.')
    bot.register_next_step_handler(message, delete_title)


def delete_title(message):
    chat_id = message.chat.id
    title = message.text
    db_delete_movie(title=title)
    bot.send_message(chat_id,
                     f'Фильм {title} удалён из базы данных.'
                     )


@bot.message_handler(commands=['фильмы',])
def show_movies(message):
    chat_id = message.chat.id
    movies = cursor.execute('SELECT title, search_date FROM movies;')
    movies_list = movies.fetchall()
    movies_str = "\n".join([str(movie) for movie in movies_list])
    bot.send_message(chat_id, movies_str)


@bot.message_handler(commands=['добавить',])
def welcome(message):
    chat_id = message.chat.id
    bot.send_message(chat_id,
                     'Введите название фильма.')
    bot.register_next_step_handler(message, save_title)


def save_title(message):
    chat_id = message.chat.id
    title = message.text
    bot.send_message(chat_id,
                     'Введите дату просмотра.')
    bot.register_next_step_handler(message, save_date, title)


def save_date(message, title):
    chat_id = message.chat.id
    date = message.text
    db_add_movie(title=title, search_date=date)
    bot.send_message(chat_id,
                     (f'Фильм {title} занесён в базу данных.'
                      f'\nДата просмотра: {date}.')
                     )


def main():
    bot.polling()


if __name__ == '__main__':
    main()
