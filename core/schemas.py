from dataclasses import dataclass


@dataclass
class Car:
    url: str
    name: str
    price: str
    bidfax_url: str | None
    pictures: list
