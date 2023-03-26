from urllib.parse import urljoin

import requests
from loguru import logger


class DellaDownloader:
    """Downloads della.kz pages"""

    def __init__(self) -> None:
        self.base_url = 'https://www.della.kz/'

    def load_page(
        self, url: str | None = None, path: str | None = None
    ) -> str | None:
        """Loads della.kz page

        Args:
            url (str | None): url of della.kz page, optional
            path (str | None): path of della.kz page, for
                example, /search/a98bdeflolh0i230301l230516k0m1.html

        Raises:
            ValueError: Page or path must be specified
            ValueError: Only one of page or path must be specified

        Returns:
            str: html source of della.kz page
        """
        if not url and not path:
            raise ValueError('Page or path must be specified')
        if url and path:
            raise ValueError('Only one of page or path must be specified')
        if not url:
            url = urljoin(self.base_url, path)

        try:
            result = requests.get(url, timeout=10)
        except requests.exceptions.RequestException:
            logger.exception('Error loading page')
            return None
        if result.ok:
            return result.text

        logger.error(f'Error loading page: {result.status_code}')
        return None
