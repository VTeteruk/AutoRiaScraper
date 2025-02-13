import asyncio
import json
import os
import sqlite3

from core.config import configure_logging
from core.schemas import Car
from settings import Settings
from telegram.telegram import send_telegram_notification


configure_logging()


def connect_db() -> sqlite3.connect:
    if not os.path.exists(Settings.DB_PATH):
        conn = sqlite3.connect(Settings.DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS cars (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            name TEXT NOT NULL,
            price TEXT NOT NULL,
            bidfax_url TEXT,
            pictures TEXT
        )
        """)

        conn.commit()
        conn.close()

    return sqlite3.connect(Settings.DB_PATH)


def add_new_car(cursor, url: str, name: str, price: str, bidfax_url: str, pictures: list) -> None:
    cursor.execute(
        "INSERT INTO cars (url, name, price, bidfax_url, pictures) VALUES (?, ?, ?, ?, ?)",
        (url, name, price, bidfax_url, json.dumps(pictures))
    )

    asyncio.run(send_telegram_notification(url, name, price, bidfax_url, pictures))


def check_price(cursor, url: str, name: str, price: str, bidfax_url: str, pictures: list) -> None:
    cursor.execute("SELECT price FROM cars WHERE url = ?", (url,))
    current_price = cursor.fetchone()

    if current_price[0] != price:
        cursor.execute("UPDATE cars SET price = ? WHERE url = ?", (price, url))
        asyncio.run(send_telegram_notification(url, name, current_price[0], bidfax_url, pictures, changed_price=price))


def check_unavailable_cars(cursor, data: list[Car]) -> None:
    scraped_urls = [car.url for car in data]
    cursor.execute("SELECT url FROM cars")
    existing_cars = cursor.fetchall()

    for existing_car in existing_cars:
        existing_car = existing_car[0]
        if existing_car not in scraped_urls:
            cursor.execute("SELECT url, name, price, bidfax_url, pictures FROM cars WHERE url = ?", (existing_car,))
            *car_data, pictures = cursor.fetchone()
            asyncio.run(send_telegram_notification(*car_data, json.loads(pictures), not_available=True))

            cursor.execute("DELETE FROM cars WHERE url = ?", (existing_car,))


def save_data_to_db_send_notifications(conn: sqlite3.connect, data: list[Car]) -> None:
    cursor = conn.cursor()

    try:
        for car in data:
            cursor.execute("SELECT id FROM cars WHERE url = ?", (car.url,))
            existing_car = cursor.fetchone()

            url, name, price, bidfax_url, pictures = car.url, car.name, car.price, car.bidfax_url, car.pictures

            if not existing_car:
                add_new_car(cursor, url, name, price, bidfax_url, pictures)
            else:
                check_price(cursor, url, name, price, bidfax_url, pictures)

        check_unavailable_cars(cursor, data)
    finally:
        conn.commit()
        conn.close()
