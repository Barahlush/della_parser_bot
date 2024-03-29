from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from urllib.parse import urljoin

from bs4.element import Tag

SECONDS_IN_MINUTE, SECONDS_IN_HOUR = 60, 3600


@dataclass
class RoutePoint:
    city: str
    country: str
    region: str

    def __repr__(self) -> str:
        return f'{self.city}, {self.country}, {self.region}'


# The code contains a class that represents a search card.
# The class has a number of attributes that describe the search card.
# The class has a special method __eq__ that compares search cards by their
# order_id. This is needed to check that the search card was added to the
# database.
# The class has a special method __repr__ that prints the search card in a
# readable format.


@dataclass
class SearchCard:
    order_id: str
    creation_time: datetime | None
    country: str | None
    from_location: RoutePoint
    to_location: RoutePoint
    distance: str | None
    truck_type: str | None
    weight: str | None
    volume: str | None
    cargo_type: str | None
    date: str | None
    link: str

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, SearchCard):
            return NotImplemented
        return self.order_id == other.order_id

    def __repr__(self) -> str:
        if self.creation_time:
            created_time_ago = (
                datetime.now() - self.creation_time
            ).total_seconds()
            if created_time_ago < SECONDS_IN_MINUTE:
                created_ago = f'{created_time_ago:.0f} seconds ago'
            elif created_time_ago < SECONDS_IN_HOUR:
                created_ago = (
                    f'{created_time_ago // SECONDS_IN_MINUTE:.0f} minutes ago'
                )
            else:
                created_ago = (
                    f'{created_time_ago // SECONDS_IN_HOUR:.0f} hours ago'
                )
        else:
            created_ago = 'today'

        return (
            f'(Creation time: {created_ago}\n'
            f'From: {self.from_location}\n'
            f'To: {self.to_location}\n'
            f'Distance: {self.distance}\n'
            f'Date: {self.date}\n'
            f'Truck type: {self.truck_type}\t'
            f'Weight: {self.weight}\t'
            f'Volume: {self.volume}\t'
            f'Cargo type: {self.cargo_type}\n'
            f'Link: {self.link})\n'
        )


class DellaParser:
    """Parses della.kz search page"""

    def parse(self, html: str) -> list[SearchCard]:
        """Parses della.kz search page

        Args:
            html (str): html of della.kz search page

        Returns:
            list[SearchCard]: list of parsed cards
        """
        from bs4 import BeautifulSoup

        soup = BeautifulSoup(html, 'html.parser')
        cards = soup.select('.request_card')
        return [self.extract_info(card) for card in cards]

    def extract_info(self, card_tag: Tag) -> SearchCard:
        """Extracts information from the card tag

        Args:
            card_tag (Tag): card tag

        Returns:
            SearchCard: extracted information
        """

        base_url = 'https://www.della.kz/'

        def extract_text(tag: Tag, selector: str) -> str | None:
            if selected_tag := tag.select_one(selector):
                return str(selected_tag.text.strip())
            return None

        def parse_route_location(location: Tag) -> RoutePoint:
            """Extracts city, country and region from the card route location.

            Args:
                location (Tag): route location tag (span)

            Returns:
                dict: city, country and region
            """
            city_and_country, region = location.text.strip(), location['title']
            city = city_and_country.split(' ')[0]
            country = city_and_country.split(' ')[1][1:-1]
            return RoutePoint(city, country, region)

        # Extract time of creation
        if time_string := extract_text(card_tag, '.diff_minutes'):
            minutes = int(time_string.split()[0])
            time_of_creation = datetime.now() - timedelta(minutes=minutes)
        elif time_string := extract_text(card_tag, '.diff_seconds'):
            seconds = int(time_string.split()[0])
            time_of_creation = datetime.now() - timedelta(seconds=seconds)
        else:
            time_of_creation = None

        # Extract country name
        country_name = extract_text(card_tag, '.country_abbr')
        if country_name:
            country_name = country_name.upper()

        # Extract route (source and destination)
        from_location_tag, to_location_tag = card_tag.select(
            '.request_route span'
        )[::2][:2]
        from_location, to_location = parse_route_location(
            from_location_tag
        ), parse_route_location(to_location_tag)

        # Extract cargo type
        cargo_type = extract_text(card_tag, '.cargo_type')

        # Extract date
        date = extract_text(card_tag, '.date_add')

        # Extract link to the application
        if path := card_tag.select_one('.request_distance').get('href', None):
            link = urljoin(base_url, path)
        else:
            raise ValueError('Link to the card is not found')

        # Extract truck type
        truck_type = extract_text(card_tag, '.truck_type')

        # Extract weight
        weight = extract_text(card_tag, '.weight')

        # Extract volume
        volume = extract_text(card_tag, '.cube')

        # Extract distance
        distance = extract_text(card_tag, 'a.distance')

        order_id = link.split('=')[-1]

        return SearchCard(
            order_id,
            time_of_creation,
            country_name,
            from_location,
            to_location,
            distance,
            truck_type,
            weight,
            volume,
            cargo_type,
            date,
            link,
        )
