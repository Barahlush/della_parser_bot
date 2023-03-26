import datetime

from peewee import (
    CharField,
    DateField,
    Model,
    SqliteDatabase,
)

from della_parser_bot.config import DATABASE_PATH

db = SqliteDatabase(DATABASE_PATH, pragmas={'foreign_keys': 1})


class BaseModel(Model):  # type: ignore
    creation_time = DateField(default=datetime.datetime.now)

    class Meta:
        database = db


class Filter(BaseModel):
    country_from = CharField()
    country_to = CharField()


class User(BaseModel):
    username = CharField(unique=True)
    chat_id = CharField(unique=True)

    def __str__(self) -> str:
        return str(self.username)

    def __repr(self) -> str:
        return str(self.username)
