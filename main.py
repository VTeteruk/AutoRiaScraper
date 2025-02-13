import logging
import time

from core.config import configure_logging
from core.schemas import Car
from db.db import connect_db, save_data_to_db_send_notifications
from scrapers.car_links_scraper import CarLinksScraper
from settings import Settings
from validation.validator import Validator

configure_logging()


def scrape_data() -> list[Car]:
    scraper = CarLinksScraper()
    data = scraper.scrape_cars()

    return Validator().validate(data)


def main() -> None:
    while True:
        logging.info("Scrape Cars...")
        validated_data = scrape_data()

        logging.info("Connecting to DB...")
        conn = connect_db()

        logging.info("Saving data to DB & Sending notifications...")
        save_data_to_db_send_notifications(conn, validated_data)

        logging.info("Waiting for the next start...")
        time.sleep(Settings.TIME_BETWEEN_RUNS)


if __name__ == "__main__":
    main()
