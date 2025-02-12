import logging

from core.config import configure_logging
from core.schemas import Car
from db.db import connect_db, save_data_to_db
from scrapers.car_links_scraper import CarLinksScraper
from validation.validator import Validator

configure_logging()


def scrape_data() -> list[Car]:
    scraper = CarLinksScraper()
    data = scraper.scrape_cars()

    return Validator().validate(data)


def main() -> None:
    logging.info("Scrape Cars...")
    validated_data = scrape_data()

    logging.info("Connecting to DB...")
    conn = connect_db()

    logging.info("Saving data to DB...")
    save_data_to_db(conn, validated_data)


if __name__ == "__main__":
    main()
