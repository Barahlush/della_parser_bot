from pytest import fixture

from della_parser_bot.parser import DellaParser


@fixture
def test_page() -> str:
    with open('tests/data/test_page.html') as f:
        return f.read()


@fixture
def test_card_repr() -> str:
    return """From: Костанай, KZ, Костанайская  обл.
To: Челябинск, RU, Челябинская  обл.
Distance: 642 км
Date: 16.03
Truck type: рефрижератор	Weight: 16 т	Volume: 80 м³	Cargo type: тара
Link: https://www.della.kz/distance/?cities=1237,387,387,1237&rc=23072144341435538)\n"""


def test_parser(test_page: str, test_card_repr: str) -> None:
    parser = DellaParser()

    result = parser.parse(test_page)
    assert len(result) == 26

    first_card = result[0]
    first_line_end = str(first_card).find('\n')
    assert str(first_card)[first_line_end + 1 :] == test_card_repr
    assert str(first_card.from_location) == 'Костанай, KZ, Костанайская  обл.'
    assert first_card.from_location.city == 'Костанай'
    assert first_card.from_location.country == 'KZ'
    assert first_card.from_location.region == 'Костанайская  обл.'
    assert first_card.to_location.city == 'Челябинск'
    assert first_card.to_location.country == 'RU'
    assert first_card.to_location.region == 'Челябинская  обл.'
    assert first_card.distance == '642 км'
    assert first_card.date == '16.03'
    assert first_card.truck_type == 'рефрижератор'
    assert first_card.weight == '16 т'
    assert first_card.volume == '80 м³'
    assert first_card.cargo_type == 'тара'
    assert first_card.country == 'KZ'
    assert (
        first_card.link
        == 'https://www.della.kz/distance/?cities=1237,387,387,1237&rc=23072144341435538'
    )

    second_card = result[2]
    assert second_card.distance is None
    assert second_card.volume is None
