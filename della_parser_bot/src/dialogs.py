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


class DialogueFilter:
    def __init__(
        self,
        name: str,
        text: str,
        filter_type: str,
        value: str | int | bool | float,
    ):
        self.name = name
        self.text = text
        self.filter_type = filter_type
        self.value = value

    def __repr__(self) -> str:
        return self.name
