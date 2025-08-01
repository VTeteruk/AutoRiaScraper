import asyncio
import logging

import aiohttp
from bs4 import BeautifulSoup

from core.config import configure_logging
from core.schemas import Car
from .car_details_scraper import CarDetailsScraper

configure_logging()


class CarScraper(CarDetailsScraper):
    @staticmethod
    async def fetch_url_content(session, url: str, timeout=10000) -> str:
        for _ in range(3):
            try:
                async with session.get(url, timeout=timeout) as response:
                    return await response.text()
            except Exception as ex:
                logging.error(ex)

    async def create_car_instance(self, session: aiohttp.ClientSession, url: str) -> Car:
        try:
            text_response = await self.fetch_url_content(session, url)
            soup = BeautifulSoup(text_response, "html.parser")

            property_data = self.get_car_data(soup)
            if property_data["pictures"] and property_data["name"] and property_data["price"]:
                return Car(
                    url=url,
                    **property_data
                )
        except Exception as ex:
            logging.error(f"{url}: {ex}")

    async def create_coroutines(self, session: aiohttp.ClientSession, links: list[str]) -> list[Car]:
        coroutines = [
            self.create_car_instance(session, link)
            for link in links
        ]
        return await asyncio.gather(*coroutines)
