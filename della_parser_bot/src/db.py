from della_parser_bot.src.models import Filter, User, db


def get_user_filters(user: User) -> list[Filter]:
    with db:
        return list(user.filters)
