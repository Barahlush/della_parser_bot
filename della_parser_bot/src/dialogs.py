from abc import abstractmethod
from collections.abc import Callable
from typing import Any

from telebot.service_utils import quick_markup
from telebot.types import InlineKeyboardMarkup


class Phrase:
    @abstractmethod
    def markup(self) -> InlineKeyboardMarkup:
        pass

    @abstractmethod
    def callback(self, call: Callable[..., Any]) -> None:
        pass


class AddFilter(Phrase):
    def markup(self) -> InlineKeyboardMarkup:
        return quick_markup(
            [
                [
                    {
                        'text': 'Add filter',
                        'callback_data': 'add_filter',
                    }
                ]
            ]
        )

    def callback(self, call: Callable[..., Any]) -> None:
        pass
