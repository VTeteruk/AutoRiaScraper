import os

from fake_useragent import UserAgent
from dotenv import load_dotenv


load_dotenv()


class Settings:
    # SCRAPER SETTINGS
    TIME_BETWEEN_RUNS = 600  # 10 min

    # LINKS
    BASE_URL = "https://auto.ria.com/"
    BASE_SEARCH_URL = "https://auto.ria.com/search/?indexName=auto&categories.main.id=1&brand.id[0]=79&model.id[0]=2104&country.import.usa.not=0&price.currency=1&abroad.not=0&custom.not=1&size=100&page="

    # HEADERS
    HEADERS = {
        "user-agent": UserAgent().random
    }

    # VALIDATOR SETTINGS
    BIDFAX_URL_IS_REQUIRED = False

    # DB SETTINGS
    DB_PATH = "cars.db"

    # TELEGRAM BOT SETTINGS
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
    MAX_PICTURES_IN_TELEGRAM = 10  # 10 is max
    TELEGRAM_NOTIFICATION_SLEEP_TIME = 30  # seconds
    TELEGRAM_NOTIFICATION_RETRIES = 3
