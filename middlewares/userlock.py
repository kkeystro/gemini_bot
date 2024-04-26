from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject
from db.redb import check_ul


class ThrottlingMiddleware(BaseMiddleware):

    async def __call__(self,
                       handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: Message,
                       data: Dict[str, Any]
                       ) -> Any:
        user = str(event.from_user.id)

        check_user = await check_ul(user)

        if check_user:
            return await event.answer('Wait a little')

        return await handler(event, data)
