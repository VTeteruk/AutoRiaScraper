import logging
from dataclasses import fields

from price_parser import Price

from core.config import configure_logging
from core.schemas import Car
from settings import Settings

configure_logging()


class Validator:
    def __init__(self) -> None:
        self.validated_data = []

    @staticmethod
    def get_types() -> dict:
        return {
            item.name: item.type
            for item in fields(Car)
        }

    def validate_types(self, item: Car) -> bool:
        car_fields = self.get_types()

        for field_name in car_fields:
            value = item.__getattribute__(field_name)

            if not isinstance(value, car_fields.get(field_name)):
                return False
        return True

    @staticmethod
    def prettify_price(price: str) -> str:
        parsed_price = Price.fromstring(price)
        return f"{parsed_price.amount} {parsed_price.currency}"

    def validate(self, car_data: list[Car]) -> list[Car]:
        for item in car_data:
            try:

                if item.url in [data.url for data in self.validated_data]:
                    continue

                if not item.bidfax_url and Settings.BIDFAX_URL_IS_REQUIRED:
                    continue

                if not self.validate_types(item):
                    continue

                item.price = self.prettify_price(item.price)

                self.validated_data.append(item)

            except Exception as ex:
                logging.error(ex)
                continue

        return self.validated_data
