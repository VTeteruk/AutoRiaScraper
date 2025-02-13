# Auto-Ria Scraper
## Overview
This Python script scrapes information about used cars from auto.ria.com, tracks price changes, and sends notifications about new listings, price updates, and unavailable cars via Telegram. It uses Selenium for web scraping, SQLite3 for data storage, and aiogram for Telegram notifications.
___
## Features
* **Car Listings Scraper**: Collects information on used cars such as make, model, price, and photos from auto.ria.com. The script processes multiple pages to gather all available listings.

* **Price Change Tracker:** The script compares new listings with previously stored data and tracks price changes.

* **Unavailable Listings:** If a car is no longer available, the script sends a notification via Telegram.

* **SQLite3 Database:** Stores scraped car data and tracks changes to prices and availability.
___
## Requirements
1. [Python 3.x](https://www.python.org/downloads/) must be installed.
2. Copy the project.
3. Add the following variables to the .env file:
    ```
    TELEGRAM_TOKEN=your-telegram-bot-token
    TELEGRAM_CHAT_ID=your-chat-id
   ```
4. Create and activate your virtual environment:
   * For Mac/Linux:
     ```bash
     python3 -m venv venv
     ```
     ```bash
     source venv/bin/activate
     ```
   * For Windows:
     ```bash
     python -m venv venv
     ```
     ```bash
     venv\Scripts\activate.bat
     ```
5. Install the required Python libraries using the following command:
   ```bash
   pip install -r requirements.txt
___
## Usage
Run the script using the following command:

```bash
python -m main
```
___
## Settings
You can customize the script behavior by modifying the settings in the `settings.py` file.


**NOTE:**

As this project uses asynchronous scraping, there may be instances where adding a proxy is necessary to bypass bot detection mechanisms.