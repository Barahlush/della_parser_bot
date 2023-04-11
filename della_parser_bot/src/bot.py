import time

import telebot
from loguru import logger
from peewee import SqliteDatabase
from telebot.storage import StateRedisStorage

from della_parser_bot.config import DATABASE_PATH, TELEGRAM_BOT_API_TOKEN
from della_parser_bot.src.filters import add_filters_to_bot
from della_parser_bot.src.messages import messages
from della_parser_bot.src.models import Filter, User

db = SqliteDatabase(DATABASE_PATH, pragmas={'foreign_keys': 1})

storage = StateRedisStorage()

bot = telebot.TeleBot(TELEGRAM_BOT_API_TOKEN, state_storage=storage)
add_filters_to_bot(bot)


@bot.message_handler(commands=['start'])   # type: ignore
def start_message(message: telebot.types.Message) -> None:
    bot.delete_message(message.chat.id, message.message_id)
    bot.send_message(
        message.chat.id,
        messages['start'],
    )
    with db:
        try:
            db.create_tables([User, Filter])
            User.get_or_create(
                username=message.from_user.username, chat_id=message.chat.id
            )
            logger.info(message.chat.id)
        except Exception:
            logger.exception(messages['unknown_error'])


# This code is responsible for generating a list of users from the database
# and sending it to the administrator. The list is cached in the database.
@bot.message_handler(commands=['list_users'])   # type: ignore
def list_users(message: telebot.types.Message) -> None:
    if message.from_user.username != 'della':
        bot.send_message(message.chat.id, messages['not_admin'])
        return
    with db:
        users = User.select()
        if not users:
            bot.send_message(message.chat.id, messages['no_users'])
            return
        response_message = 'Список пользователей:\n'
        for user in users:
            response_message += f'{user}\n'
        bot.send_message(message.chat.id, response_message)


# bot.register_callback_query_handler(


if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            logger.exception(f'Error polling for messages: {e}')
            time.sleep(5)
