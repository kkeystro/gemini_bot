import traceback

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from rest import generate_text
from db.redb import ReStorage
from serialiser import serialise as s

router = Router()

storage = ReStorage(chat_id=67857)

m1 = "Ответы даю максимально развёрнуто и подробно, на русском языке, если не необходимо или указано обратное"


@router.message(Command("start"))
async def cmd_start(message: Message):
    await storage.delkeys(key=str(message.from_user.id))
    await message.answer(
        "Добро пожаловать в мир генеративного ИИ!",
    )


@router.message(Command("clear"))
async def cmd_start(message: Message):
    await storage.delkeys(key=str(message.from_user.id))
    await message.answer(
        "История очищена",
    )


@router.message(F.text)
async def message_with_text(message: Message):
    try:
        msg = await message.answer("Думаю...")
        await storage.pushr(key=str(message.from_user.id), value=s(message.text, "user"))
        response = await generate_text(uid=message.from_user.id)
        # await storage.pushr(key=str(message.from_user.id), value=s(message.text, "user"))
        await storage.pushr(key=str(message.from_user.id), value=s(response, "model"))
        await msg.edit_text(response)
    except Exception:
        traceback.print_exc()
        await storage.delkeys(key=str(message.from_user.id))
