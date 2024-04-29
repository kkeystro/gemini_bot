from config_reader import config
import traceback
from aiogram import Router, F, Bot
from aiogram.types import Message
from rest import generate_text
import db.redb as storage
from serialiser import serialise as s
from mdfuck import escape_markdown_v2
from imageshit.converter import convert_to_base64
from fucked_state_machine import UserStates

router = Router()


@router.message(UserStates.user_premium, F.photo)
async def message_with_text(message: Message):
    await storage.set_ul(str(message.from_user.id))
    msg = await message.answer("Analysing...")
    try:
        await Bot(token=config.bot_token.get_secret_value()).download(message.photo[-1], destination=f'imageshit/{str(message.from_user.id)}.jpeg')
        image_base64 = convert_to_base64(str(message.from_user.id))
        await storage.pushr(key=str(message.from_user.id), value=s(message.text, "user", image=image_base64))
        response = await generate_text(uid=message.from_user.id)
        print(escape_markdown_v2(response))
        await storage.pushr(key=str(message.from_user.id), value=s(response, "model"))
        await msg.edit_text(escape_markdown_v2(response))
        await storage.unlock(str(message.from_user.id))

    except Exception:
        traceback.print_exc()
        await msg.edit_text("Text generation error")
        await storage.unlock(str(message.from_user.id))
        await storage.delkey(key=str(message.from_user.id))


@router.message(UserStates.user_not_premium, F.photo)
async def message_with_text(message: Message):
    await storage.set_ul(str(message.from_user.id))
    await message.answer("Функция работы с изображениями доступна только /premium пользователям")
    await storage.unlock(str(message.from_user.id))
