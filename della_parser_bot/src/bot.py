import time

import telebot
from loguru import logger
from peewee import SqliteDatabase

from della_parser_bot.config import DATABASE_PATH, TELEGRAM_BOT_API_TOKEN
from della_parser_bot.src.messages import messages
from della_parser_bot.src.models import Filter, User

db = SqliteDatabase(DATABASE_PATH, pragmas={'foreign_keys': 1})

bot = telebot.TeleBot(TELEGRAM_BOT_API_TOKEN)


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
            User.create(
                username=message.from_user.username, chat_id=message.chat.id
            )
            logger.info(message.chat.id)
        except Exception:
            logger.exception(messages['unknown_error'])


if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            logger.exception(f'Error polling for messages: {e}')
            time.sleep(5)
