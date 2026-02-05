def ask_for_input(bot, message, prompt, next_handler, *args):
    """
    Запрашивает у пользователя данные и передаёт их в следующий обработчик.

    :param message: Объект сообщения от пользователя.
    :param prompt: Текст запроса (например, "Введите название фильма").
    :param next_handler: Функция, которая обработает ввод пользователя.
    :param args: Дополнительные аргументы для next_handler.
    """
    chat_id = message.chat.id
    bot.send_message(chat_id, prompt)
    bot.register_next_step_handler(message, next_handler, *args)