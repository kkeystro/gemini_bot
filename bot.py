import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties


import mainpatcher


async def main():
    default = DefaultBotProperties(parse_mode=None)
    bot = Bot(token="7164466516:AAFBaaf7Or2TTNkAAxeffDhfb67S300nPg0", default=default)
    dp = Dispatcher()
    dp.include_routers(mainpatcher.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
