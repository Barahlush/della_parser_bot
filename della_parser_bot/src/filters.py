import telebot
from telebot.callback_data import CallbackData

from della_parser_bot.src.db import get_user_filters
from della_parser_bot.src.messages import messages
from della_parser_bot.src.models import Filter, User


def show_filters(message: telebot.types.Message, bot: telebot.TeleBot) -> None:
    filters = get_user_filters(User.get(User.chat_id == message.chat.id))
    if not filters:
        response_message = 'У вас нет активных фильтров. Самое время добавить!'
    else:
        response_message = 'Ваши фильтры:\n'
        for i, filt in enumerate(filters):
            response_message += f'Фильтр {i}:\n{filt}\n\n'

    bot.send_message(
        message.chat.id,
        response_message,
        reply_markup=filter_markup_start(filters),
    )
    bot.delete_message(message.chat.id, message.message_id)


def filter_markup_start(
    user_filters: list[Filter],
) -> telebot.types.InlineKeyboardMarkup:
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(
        telebot.types.InlineKeyboardButton(
            'Добавить фильтр', callback_data='add_filter'
        )
    )
    if user_filters:
        markup.add(
            telebot.types.InlineKeyboardButton(
                'Удалить фильтр', callback_data='remove_filter'
            )
        )
    return markup


filter_fields = ['filter_id', 'country_from', 'country_to']

filter_factory = CallbackData(*filter_fields, prefix='filters')
countries = [
    {'name': 'Россия', 'code': 'RU'},
    {'name': 'Украина', 'code': 'UA'},
    {'name': 'Беларусь', 'code': 'BY'},
    {'name': 'Казахстан', 'code': 'KZ'},
    {'name': 'Киргизия', 'code': 'KG'},
    {'name': 'Таджикистан', 'code': 'TJ'},
    {'name': 'Армения', 'code': 'AM'},
]


def filter_markup_add(
    current_filter: Filter | None = None,
) -> telebot.types.InlineKeyboardMarkup:
    if not current_filter:
        current_filter = Filter()
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(
        telebot.types.InlineKeyboardButton(
            f'Страна отправления: {current_filter.country_from}',
            callback_data=filter_factory.new(filter_id=current_filter.id),
        )
    )
    markup.add(
        telebot.types.InlineKeyboardButton(
            f'Страна прибытия: {current_filter.country_to}',
            callback_data=filter_factory.new(filter_id=current_filter.id),
        )
    )

    markup.add(
        telebot.types.InlineKeyboardButton('Отмена', callback_data='cancel')
    )
    markup.add(
        telebot.types.InlineKeyboardButton('Готово', callback_data='ok')
    )
    return markup


def add_filter(
    call: telebot.types.CallbackQuery, bot: telebot.TeleBot
) -> None:
    try:
        bot.send_message(
            call.message.chat.id,
            messages['add_filter'],
            reply_markup=filter_markup('add', []),
        )
    except Exception:
        logger.exception(messages['unknown_error'])
        bot.answer_callback_query(
            call.id,
            messages['unknown_error'],
        )
