from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

import db.redb as storage

router = Router()


@router.message(Command("clear"))
async def cmd_clear(message: Message):
    await storage.delkey(key=str(message.from_user.id))
    await message.answer(
        "Hystory cleared",
    )
