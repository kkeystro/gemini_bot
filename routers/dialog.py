import traceback

from aiogram import Router, F
from aiogram.types import Message

import db.redb as storage
from fucked_state_machine import UserStates
from mdfuck import escape_markdown_v2
from rest import generate_text
from serialiser import serialise as s

router = Router()


@router.message(UserStates.user_not_premium, F.text)
async def message_with_text(message: Message):
    await storage.set_ul(str(message.from_user.id))
    msg = await message.answer("Generating...")
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
        await storage.unlock(str(message.from_user.id))
        await storage.delkey(key=str(message.from_user.id))
