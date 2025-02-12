from dataclasses import fields

from price_parser import Price

from core.schemas import Car
from settings import Settings


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

    def prettify_price(self, price: str) -> str:
        parsed_price = Price.fromstring(price)
        return f"{parsed_price.amount} {parsed_price.currency}"

    def validate(self, car_data: list[Car]) -> list[Car]:
        for item in car_data:

            if item.url in self.validated_data:
                continue

            if not item.bidfax_url and Settings.BIDFAX_URL_IS_REQUIRED:
                continue

            if not self.validate_types(item):
                continue

            item.price = self.prettify_price(item.price)

            self.validated_data.append(item)

        return self.validated_data
