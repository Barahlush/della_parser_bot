import telebot
from telebot.callback_data import CallbackData, CallbackDataFilter
from telebot import AdvancedCustomFilter, types

from della_parser_bot.src.db import get_user_filters
from della_parser_bot.src.messages import messages
from della_parser_bot.src.models import Filter, User
from telebot.handler_backends import State, StatesGroup   # States
from loguru import logger


def show_filters(message: telebot.types.Message, bot: telebot.TeleBot) -> None:
    filters = get_user_filters(User.get(User.chat_id == message.chat.id))
    if not filters:
        response_message = 'У вас нет активных фильтров. Самое время добавить!'
    else:
        response_message = 'Ваши фильтры:\n'
        for i, filt in enumerate(filters):
            response_message += f'Фильтр {i}:\n{filt}\n\n'

    bot.delete_message(message.chat.id, message.message_id)
    bot.send_message(
        message.chat.id,
        response_message,
        reply_markup=filter_markup_start(filters),
    )


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


filter_fields = ['id', 'field', 'value']

filter_factory = CallbackData(*filter_fields, prefix='select')
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
    user: User,
    current_filter: Filter | None = None,
) -> telebot.types.InlineKeyboardMarkup:
    if not current_filter:
        current_filter = Filter()
        current_filter.save()
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(
        telebot.types.InlineKeyboardButton(
            f'Страна отправления: {current_filter.country_from}',
            callback_data=filter_factory.new(
                id=current_filter.id, field='country_from', value=''
            ),
        )
    )
    markup.add(
        telebot.types.InlineKeyboardButton(
            f'Страна прибытия: {current_filter.country_to}',
            callback_data=filter_factory.new(
                id=current_filter.id, field='country_to', value=''
            ),
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
            reply_markup=filter_markup_add(
                User.get(username=call.from_user.username)
            ),
        )
    except Exception:
        logger.exception(messages['unknown_error'])
        bot.answer_callback_query(
            call.id,
            messages['unknown_error'],
        )


# config=filter_factory.filter(field='country_from', value=None)
def select_country(
    call: telebot.types.CallbackQuery, bot: telebot.TeleBot
) -> None:
    try:
        filter_dict = filter_factory.parse(call.data)
        filter_id = int(filter_dict['id'])
        filter_object = Filter.get(Filter.id == filter_id)
        if 'value' in filter_dict and filter_dict['value']:
            setattr(filter_object, filter_dict['field'], filter_dict['value'])
            filter_object.save()
            bot.edit_message_text(
                messages['select_country'],
                call.message.chat.id,
                call.message.message_id,
                reply_markup=filter_markup_add(
                    User.get(username=call.from_user.username), filter_object
                ),
            )
            return

        markup = telebot.types.InlineKeyboardMarkup()
        for country in countries:
            markup.add(
                telebot.types.InlineKeyboardButton(
                    country['name'],
                    callback_data=filter_factory.new(
                        id=filter_id,
                        field=filter_dict['field'],
                        value=country['code'],
                    ),
                )
            )
        bot.edit_message_text(
            messages['select_country'],
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup,
        )
    except Exception:
        logger.exception(messages['unknown_error'])
        bot.answer_callback_query(
            call.id,
            messages['unknown_error'],
        )


class FilterCallbackFilter(AdvancedCustomFilter):
    key = 'config'

    def check(
        self, call: types.CallbackQuery, config: CallbackDataFilter
    ) -> bool:
        return config.check(query=call)


def handle_filter_callbacks(
    call: telebot.types.CallbackQuery, bot: telebot.TeleBot
) -> None:
    if call.data == 'add_filter':
        add_filter(call, bot)
    # elif call.data == 'remove_filter':
    #     remove_filter(call, bot)
    # elif call.data == 'cancel':
    #     cancel(call, bot)
    # elif call.data == 'ok':
    #     ok(call, bot)
    # elif call.data.startswith('filters'):
    #     filter_callback(call, bot)


def add_filters_to_bot(bot: telebot.TeleBot) -> None:
    bot.register_message_handler(
        show_filters, commands=['filters'], pass_bot=True
    )

    bot.register_callback_query_handler(
        select_country,
        func=None,
        pass_bot=True,
        config=filter_factory.filter(field='country_from', value=''),
    )

    bot.register_callback_query_handler(
        select_country,
        func=None,
        pass_bot=True,
        config=filter_factory.filter(field='country_to', value=''),
    )

    bot.add_custom_filter(FilterCallbackFilter())
    bot.register_callback_query_handler(
        handle_filter_callbacks, lambda x: True, pass_bot=True
    )
