from dataclasses import dataclass


@dataclass
class Car:
    url: str
    name: str
    price: int
    bidfax_url: str | None
    pictures: list[str]
