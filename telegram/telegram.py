import time

from aiogram import Bot
from aiogram.exceptions import TelegramRetryAfter
from aiogram.types import InputMediaPhoto

from settings import Settings


def get_caption(
        url: str,
        name: str,
        price: str,
        bidfax_url: str,
        not_available: bool,
        changed_price: str
    ) -> str:
    if changed_price:
        message = f"<b>❗<a href='{url}'>{name}</a> new price</b>\n💰 <b><s>{price}</s> {changed_price}</b>\n"
    else:
        message = f"<b><a href='{url}'>{name}</a></b>\n💰 <b>{price}</b>\n"
    if bidfax_url:
        message += f"🇺🇸 <a href='{bidfax_url}'>bidfax</a>\n"

    if not_available:
        return f"<b>😔<a href='{url}'>{name}</a></b> is no longer available"

    return message


async def send_telegram_notification(
        url: str,
        name: str,
        price: str,
        bidfax_url: str,
        pictures: list,
        not_available: bool = False,
        changed_price: str = ""
) -> None:
    for _ in range(Settings.TELEGRAM_NOTIFICATION_RETRIES):
        try:
            caption = get_caption(url, name, price, bidfax_url, not_available, changed_price)

            media = [InputMediaPhoto(media=picture) for picture in pictures[:Settings.MAX_PICTURES_IN_TELEGRAM]]
            media[0] = InputMediaPhoto(media=pictures[0], caption=caption, parse_mode="HTML")

            async with Bot(token=Settings.TELEGRAM_TOKEN) as bot:
                await bot.send_media_group(chat_id=Settings.TELEGRAM_CHAT_ID, media=media)

            break

        except TelegramRetryAfter:
            time.sleep(Settings.TELEGRAM_NOTIFICATION_SLEEP_TIME)

        except Exception as ex:
            # TODO: add logging
            break
