import logging

from core.config import configure_logging
from scrapers.car_links_scraper import CarLinksScraper

configure_logging()


def main() -> None:
    logging.info("Scrape Cars...")
    scraper = CarLinksScraper()
    result = scraper.scrape_cars()

    print(result)
    print(len(result))


if __name__ == "__main__":
    main()
