from aiogram import Bot
from aiogram.types import InputMediaPhoto

from settings import Settings


async def send_telegram_notification(url: str, name: str, price: str, bidfax_url: str, pictures: list):
    caption = f"{name}\n💰 Ціна: {price}\n🔗 [Auto RIA]({url})\n{bidfax_url}"

    media = [InputMediaPhoto(media=picture) for picture in pictures]
    media[0].caption = caption

    async with Bot(token=Settings.TELEGRAM_TOKEN) as bot:
        await bot.send_media_group(chat_id=Settings.TELEGRAM_CHAT_ID, media=media)
