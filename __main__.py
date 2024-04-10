import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from os import environ
from keys.models import setup_db as m
import mainpatcher
#from middlewares.userlock import UserLockMiddleware


async def main():
    default = DefaultBotProperties(parse_mode=None)
    bot = Bot(token=environ.get("BOT_TOKEN"))
    dp = Dispatcher()
    dp.include_routers(mainpatcher.router)
    #dp.message.middleware(UserLockMiddleware())

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
    asyncio.run(m())
