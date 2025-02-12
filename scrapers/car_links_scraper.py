import asyncio
import math
import re

import aiohttp
from bs4 import BeautifulSoup

from core.schemas import Car
from .car_scraper import CarScraper
from .settings import Settings


class CarLinksScraper(CarScraper):
    def __init__(self) -> None:
        self.cars: list[Car] = []

    async def get_cars_links(
            self, session: aiohttp.ClientSession, url: str
    ) -> list[str]:
        text_response = await self.fetch_url_content(session, url)
        soup = BeautifulSoup(text_response, "html.parser")

        links = soup.find_all("a", {"class": "m-link-ticket"})

        return [link.get("href") for link in links]

    @staticmethod
    def get_cards_per_page() -> int:
        return int(re.findall(r"size=([0-9]+)", Settings.BASE_SEARCH_URL)[0])

    async def get_max_page_number_async(self, session: aiohttp.ClientSession, url: str) -> int:
        text_response = await self.fetch_url_content(session, url)
        soup = BeautifulSoup(text_response, "html.parser")

        try:
            # Getting total count of listings
            scripts = " ".join(str(script) for script in soup.find_all("script"))
            total_count = int(re.findall(r"resultsCount\s*=\s*Number\(([0-9]+)\)", scripts)[0])
            return math.ceil(total_count / self.get_cards_per_page())
        except (IndexError, ValueError, TypeError):
            # In case page has no pagination
            return 0

    async def process_links_async(self) -> list[Car]:
        async with aiohttp.ClientSession(headers=Settings.HEADERS) as session:
            # TODO: add logging
            max_page_number = await self.get_max_page_number_async(session, f"{Settings.BASE_SEARCH_URL}{0}")
            for page_index in range(max_page_number):
                links = await self.get_cars_links(session, f"{Settings.BASE_SEARCH_URL}{page_index}")

                try:
                    self.cars += await self.create_coroutines(session, links)
                except Exception as ex:
                    print(ex)  # TODO: add logger
        return self.cars

    def scrape_cars(self) -> list[Car]:
        return asyncio.run(self.process_links_async())
