import traceback
from keys.requests import add_api_key, get_good_key
from keys.checker import check_key
from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.types import Message
from rest import generate_text
import db.redb as storage
from serialiser import serialise as s
from mdfuck import escape_markdown_v2

router = Router()


@router.message(F.text)
async def message_with_text(message: Message):
    await storage.set_ul(str(message.from_user.id))
    msg = await message.answer("Думаю")
    try:
        await storage.pushr(key=str(message.from_user.id), value=s(message.text, "user"))
        response = await generate_text(uid=message.from_user.id)
        print(escape_markdown_v2(response))
        await storage.pushr(key=str(message.from_user.id), value=s(response, "model"))
        await msg.edit_text(escape_markdown_v2(response))
        await storage.unlock(str(message.from_user.id))

    except Exception:
        traceback.print_exc()
        await msg.edit_text("Text generation error")
        await storage.delkey(key=str(message.from_user.id))
