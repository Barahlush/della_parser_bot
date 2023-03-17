import datetime

from peewee import (
    BooleanField,
    CharField,
    DateField,
    ForeignKeyField,
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
    country = CharField()
    city = CharField()
    cargo_type = CharField()
    truck_type = CharField()
    weight = CharField()
    volume = CharField()
    date = DateField()
    distance = CharField()
    is_active = BooleanField(default=True)


class User(BaseModel):
    username = CharField(unique=True)
    chat_id = CharField(unique=True)
    filters = ForeignKeyField(Filter, null=True, default=None)
