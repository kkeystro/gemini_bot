import traceback
from keys.keysdb import add_api_key, get_good_key
from keys.checker import check_key
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from rest import generate_text
from db.redb import ReStorage
from serialiser import serialise as s

router = Router()

storage = ReStorage(chat_id=67857)


@router.message(Command("start"))
async def cmd_start(message: Message):
    await storage.delkey(key=str(message.from_user.id))
    await message.answer(
        "Добро пожаловать в мир генеративного ИИ!",
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


@router.message(F.text)
async def message_with_text(message: Message):
    msg = await message.answer("Думаю...")
    try:
        await storage.pushr(key=str(message.from_user.id), value=s(message.text, "user"))
        response = await generate_text(uid=message.from_user.id)
        await storage.pushr(key=str(message.from_user.id), value=s(response, "model"))
        await msg.edit_text(response)
    except Exception:
        traceback.print_exc()
        await msg.edit_text("Text generation error")
        await storage.delkey(key=str(message.from_user.id))
