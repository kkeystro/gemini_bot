from keys.requests import add_api_key, get_good_key
from keys.checker import check_key
from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.types import Message
import db.redb as storage

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    await storage.delkey(key=str(message.from_user.id))
    await message.answer(
        "Добро пожаловать в мир генеративного ИИ",
    )


@router.message(Command("clear"))
async def cmd_clear(message: Message):
    await storage.delkey(key=str(message.from_user.id))
    await message.answer(
        "История очищена",
    )


@router.message(Command("add"))
async def cmd_add(message: Message):
    command_text = ' '.join(message.text.split()[1:])
    if await check_key(command_text):
        await add_api_key(command_text)
        await message.answer(
            "Ключ добавлен",
        )
    else:
        await message.answer("Ключ недействителен")


@router.message(Command("get"))
async def cmd_add(message: Message):
    await message.answer(
        await get_good_key(),
    )
