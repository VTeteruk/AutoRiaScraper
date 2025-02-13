import logging

from core.config import configure_logging
from core.schemas import Car
from db.db import connect_db, save_data_to_db_send_notification
from scrapers.car_links_scraper import CarLinksScraper
from validation.validator import Validator

configure_logging()


def scrape_data() -> list[Car]:
    scraper = CarLinksScraper()
    data = scraper.scrape_cars()

    return Validator().validate(data)


def main() -> None:
    # logging.info("Scrape Cars...")
    # validated_data = scrape_data()

    validated_data = [
        Car(
            "https://auto.ria.com/auto_toyota_sequoia_37706752.html",
            "Toyota Sequoia 2008",
            "100 $",
            "http://google.com/",
            [
                "https://cdn0.riastatic.com/photosnew/auto/photo/toyota_sequoia__582365205fx.webp",
                "https://cdn3.riastatic.com/photosnew/auto/photo/toyota_sequoia__582365183fx.webp",
                "https://cdn0.riastatic.com/photosnew/auto/photo/toyota_sequoia__582365205fx.webp",
                "https://cdn3.riastatic.com/photosnew/auto/photo/toyota_sequoia__582365183fx.webp",
            ]
        )
    ]

    logging.info("Connecting to DB...")
    conn = connect_db()

    logging.info("Saving data to DB & Sending notifications...")
    save_data_to_db_send_notification(conn, validated_data)


if __name__ == "__main__":
    main()
