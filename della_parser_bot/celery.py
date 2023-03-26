from typing import Any

from celery import Celery
from loguru import logger
from redis import Redis

from della_parser_bot.parser.downloader import DellaDownloader
from della_parser_bot.parser.parser import DellaParser, SearchCard
from della_parser_bot.src.bot import bot
from della_parser_bot.src.models import User, db

app = Celery('della_parser_bot', broker='redis://redis:6379/0')
celery = app
page_loader = DellaDownloader()
parser = DellaParser()
redis = Redis(host='redis', port=6379, db=0)
redis.set('last_card', '')


@app.task
def parse_page() -> list[SearchCard]:
    # code to parse website and get new data
    logger.info('Start parsing..')
    page = page_loader.load_page(
        path='search/a98bd98eflolz1z2z3z4z5z6z7z8z9y1y2y3y4y5y6h0ilk0m1r50l25.html'
    )
    logger.info('Finished parsing...')
    if not page:
        return []
    cards = parser.parse(page)

    if new_cards := cards[find_card_offset(cards) :]:
        redis.set('last_card', str(new_cards[-1]))
    return new_cards


def find_card_offset(cards: list[SearchCard]) -> int:
    if not redis.get('last_card'):
        return 0
    for i, card in enumerate(cards):
        if str(card) == str(redis.get('last_card')):
            return i + 1
    return 0


@app.task
def send_message(user_id: str, message: str) -> None:
    bot.send_message(user_id, message)


@app.task
def send_messages() -> None:
    if not db.table_exists('user'):
        return
    cards = parse_page()

    users = User.select()
    for user in users:
        for card in cards:
            message = str(card)
            send_message.delay(str(user.chat_id), message)


@app.task
def run_process() -> None:
    send_messages.delay()


@app.on_after_configure.connect
def setup_periodic_tasks(sender: Any, **_kwargs: Any) -> None:
    sender.add_periodic_task(10.0, run_process.s(), name='Parse and send')
