import json
import os
import sqlite3

from settings import Settings


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


def save_data_to_db(conn: sqlite3.connect, data: list) -> None:
    cursor = conn.cursor()

    for car in data:
        cursor.execute("SELECT id FROM cars WHERE url = ?", (car.url,))
        existing_car = cursor.fetchone()

        if not existing_car:
            cursor.execute(
                "INSERT INTO cars (url, name, price, bidfax_url, pictures) VALUES (?, ?, ?, ?, ?)",
                (car.url, car.name, car.price, car.bidfax_url, json.dumps(car.pictures))
            )

    conn.commit()
    conn.close()