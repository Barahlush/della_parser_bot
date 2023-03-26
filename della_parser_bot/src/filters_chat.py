import redis
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

from della_parser_bot.src.models import Filter, User

r = redis.Redis(host='localhost', port=6379, db=0)
# define the callback functions for each button
def add_filter(call, bot):
    user_id = call.message.chat.id
    r.hset(f'user:{user_id}', 'selected_filter', '')
    keyboard = InlineKeyboardMarkup()
    keyboard.row(
        InlineKeyboardButton('Откуда', callback_data='from'),
        InlineKeyboardButton('Куда', callback_data='destination'),
    )
    keyboard.row(
        InlineKeyboardButton('Назад', callback_data='back'),
        InlineKeyboardButton('Принять', callback_data='submit'),
    )
    bot.edit_message_text(
        chat_id=user_id,
        message_id=call.message.message_id,
        text='Выберите параметры фильтра:',
        reply_markup=keyboard,
    )


countries = [
    {'name': 'Россия', 'code': 'RU'},
    {'name': 'Украина', 'code': 'UA'},
    {'name': 'Беларусь', 'code': 'BY'},
    {'name': 'Казахстан', 'code': 'KZ'},
    {'name': 'Киргизия', 'code': 'KG'},
    {'name': 'Таджикистан', 'code': 'TJ'},
    {'name': 'Армения', 'code': 'AM'},
]


def set_country(call, bot):
    user_id = call.message.chat.id
    place = call.data.split(':')[0]
    country_code = call.data.split(':')[1]
    r.hset(f'user:{user_id}', place, country_code)


def select_from(call, bot):
    user_id = call.message.chat.id
    keyboard = InlineKeyboardMarkup()
    buttons = [
        InlineKeyboardButton(
            country['name'], callback_data=f"from:{country['code']}"
        )
        for country in countries
    ]
    keyboard.row(*buttons)
    keyboard.row(InlineKeyboardButton('Back', callback_data='back'))
    r.hset(f'user:{user_id}', 'selected_filter', 'from')
    bot.edit_message_text(
        chat_id=user_id,
        message_id=call.message.message_id,
        text='Выберите страну отправления:',
        reply_markup=keyboard,
    )


def select_destination(call, bot):
    user_id = call.message.chat.id
    keyboard = InlineKeyboardMarkup()
    buttons = [
        InlineKeyboardButton(
            country['name'], callback_data=f"to:{country['code']}"
        )
        for country in countries
    ]
    keyboard.row(*buttons)
    keyboard.row(InlineKeyboardButton('Back', callback_data='back'))
    r.hset(f'user:{user_id}', 'selected_filter', 'destination')
    bot.edit_message_text(
        chat_id=user_id,
        message_id=call.message.message_id,
        text='Выберите страну назначения:',
        reply_markup=keyboard,
    )


def remove_filter(call, bot):
    user_id = call.message.chat.id
    User.update(filters=None).where(User.chat_id == user_id).execute()
    bot.send_message(chat_id=user_id, text='Фильтр удален.')


def back(call, bot):
    user_id = call.message.chat.id
    keyboard = InlineKeyboardMarkup()
    keyboard.row(
        InlineKeyboardButton('Добавить фильтр', callback_data='add_filter'),
        InlineKeyboardButton('Удалить фильтр', callback_data='remove_filter'),
        InlineKeyboardButton('Выйти', callback_data='close'),
    )
    bot.edit_message_text(
        chat_id=user_id,
        message_id=call.message.message_id,
        text='Выберите действие:',
        reply_markup=keyboard,
    )


def close(call, bot):
    user_id = call.message.chat.id
    bot.delete_message(chat_id=user_id, message_id=call.message.message_id)


def submit(call, bot):
    user_id = call.message.chat.id
    filter_data = r.hgetall(f'user:{user_id}')

    from_country = filter_data.get(b'from', '')
    if isinstance(from_country, bytes):
        from_country = from_country.decode('utf-8')

    destination = filter_data.get(b'destination', '')
    if isinstance(destination, bytes):
        destination = destination.decode('utf-8')

    filter_, _ = Filter.get_or_create(
        country_from=from_country, country_to=destination
    )
    User.update(filters=filter_).where(User.chat_id == user_id).execute()
    bot.answer_callback_query(call.id, 'Фильтр добавлен!')
    bot.delete_message(chat_id=user_id, message_id=call.message.message_id)


# define the callback query handler for the bot
def handle_query(call, bot):
    if call.data == 'add_filter':
        add_filter(call, bot)
    elif call.data == 'from':
        select_from(call, bot)
    elif call.data == 'destination':
        select_destination(call, bot)
    elif call.data == 'remove_filter':
        remove_filter(call, bot)
    elif call.data == 'back':
        back(call, bot)
    elif call.data == 'submit':
        submit(call, bot)
    elif call.data.startswith('from:') or call.data.startswith('to:'):
        set_country(call, bot)
