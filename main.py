import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
import logging
import sys
from keys.models import setup_db
import mainpatcher
from config_reader import config
#from middlewares.userlock import UserLockMiddleware


async def main():
    await setup_db()
    default = DefaultBotProperties(parse_mode=ParseMode.MARKDOWN_V2)
    bot = Bot(token=config.bot_token.get_secret_value()) #, default=default)
    dp = Dispatcher()
    dp.include_routers(mainpatcher.router)
    #dp.message.middleware(UserLockMiddleware())

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout, format="%(asctime)s %(levelname)s %(name)s %(message)s")
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
