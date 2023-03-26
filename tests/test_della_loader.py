import pytest
from bs4 import BeautifulSoup
from pytest import fixture

from della_parser_bot.parser.downloader import DellaDownloader


@fixture
def test_url() -> str:
    return 'https://www.della.kz/search/a98bdeflolh0i230301l230516k0m1.html'


@fixture
def test_path1() -> str:
    return '/search/a98bdeflolh0i230301l230516k0m1.html'


@fixture
def test_path2() -> str:
    return 'search/a98bdeflolh0i230301l230516k0m1.html'


@fixture
def bad_url() -> str:
    return '0i230301l230516k0m1.html'


def test_downloader(test_url: str) -> None:
    downloader = DellaDownloader()
    result = downloader.load_page(test_url)
    assert result is not None

    assert BeautifulSoup(result, 'html.parser')


def test_exceptions(test_url: str, test_path1: str) -> None:
    downloader = DellaDownloader()
    with pytest.raises(ValueError):
        downloader.load_page()
    with pytest.raises(ValueError):
        downloader.load_page(test_url, test_path1)


def test_path(test_path1: str, test_path2: str) -> None:
    downloader = DellaDownloader()
    result1 = downloader.load_page(path=test_path1)
    assert result1 is not None

    assert BeautifulSoup(result1, 'html.parser')
    result2 = downloader.load_page(path=test_path2)
    assert result2 is not None

    assert BeautifulSoup(result2, 'html.parser')


def test_bad_url(bad_url: str) -> None:
    downloader = DellaDownloader()
    result = downloader.load_page(bad_url)
    assert result is None
