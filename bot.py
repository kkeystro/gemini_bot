import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from os import environ


import mainpatcher


async def main():
    default = DefaultBotProperties(parse_mode=None)
    bot = Bot(token=str(environ.get("BOT_TOKEN")), default=default)
    dp = Dispatcher()
    dp.include_routers(mainpatcher.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
