from della_parser_bot.parser import downloader, parser


def test_load_parse() -> None:
    della_loader = downloader.DellaDownloader()
    della_parser = parser.DellaParser()
    result = della_loader.load_page(
        path='/search/a98bdeflolh0i230301l230516k0m1.html'
    )
    assert result is not None
    cards = della_parser.parse(result)
    assert len(cards) == 26
