import asyncio
import json
import os
import sqlite3
import time

from aiogram.exceptions import TelegramRetryAfter

from settings import Settings
from telegram.telegram import send_telegram_notification


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


def save_data_to_db_send_notification(conn: sqlite3.connect, data: list) -> None:
    cursor = conn.cursor()

    for car in data:
        cursor.execute("SELECT id FROM cars WHERE url = ?", (car.url,))
        existing_car = cursor.fetchone()

        if not existing_car:
            url, name, price, bidfax_url, pictures = car.url, car.name, car.price, car.bidfax_url, car.pictures
            cursor.execute(
                "INSERT INTO cars (url, name, price, bidfax_url, pictures) VALUES (?, ?, ?, ?, ?)",
                (url, name, price, bidfax_url, json.dumps(pictures))
            )

            for _ in range(Settings.TELEGRAM_NOTIFICATION_RETRIES):
                try:
                    asyncio.run(send_telegram_notification(url, name, price, bidfax_url, pictures))
                    break
                except TelegramRetryAfter:
                    time.sleep(Settings.TELEGRAM_NOTIFICATION_SLEEP_TIME)
                except Exception as ex:
                    # TODO: add logging
                    break

    conn.commit()
    conn.close()
