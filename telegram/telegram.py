from aiogram import Bot
from aiogram.types import InputMediaPhoto

from settings import Settings


async def send_telegram_notification(url: str, name: str, price: str, bidfax_url: str, pictures: list):
    if bidfax_url:
        caption = f"<b><a href='{url}'>{name}</a></b>\n💰 <b>{price}</b>\n🇺🇸 <a href='{bidfax_url}'>bidfax</a>\n"
    else:
        caption = f"<a href='{url}'>{name}</a>\n💰 <b>{price}</b>\n"

    media = [InputMediaPhoto(media=picture) for picture in pictures[:Settings.MAX_PICTURES_IN_TELEGRAM]]
    media[0] = InputMediaPhoto(media=pictures[0], caption=caption, parse_mode="HTML")

    async with Bot(token=Settings.TELEGRAM_TOKEN) as bot:
        await bot.send_media_group(chat_id=Settings.TELEGRAM_CHAT_ID, media=media)
