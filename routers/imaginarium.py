from config_reader import config
import traceback
from aiogram import Router, F, Bot
from aiogram.types import Message
from rest import generate_text
import db.redb as storage
from serialiser import serialise as s
from mdfuck import escape_markdown_v2
import base64
from PIL import Image
from io import BytesIO

router = Router()


@router.message(F.photo)
async def message_with_text(message: Message):
    await storage.set_ul(str(message.from_user.id))
    msg = await message.answer("Analysing...")
    try:
        photo = await Bot(token=config.bot_token.get_secret_value()).download( message.photo[-1] ,destination=BytesIO())
        photo.seek(0)
        img = Image.open(photo)
        img = img.resize((512, int(img.height*512/img.width)))
        buffered = BytesIO()
        img.save(buffered, format="JPEG")
        image_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
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
