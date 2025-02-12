import logging

from core.config import configure_logging
from scrapers.car_links_scraper import CarLinksScraper
from validation.validator import Validator

configure_logging()


def main() -> None:
    logging.info("Scrape Cars...")
    scraper = CarLinksScraper()
    data = scraper.scrape_cars()

    validated_data = Validator().validate(data)


if __name__ == "__main__":
    main()
