import traceback
from keys.requests import add_api_key, get_good_key
from keys.checker import check_key
from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.types import Message
from rest import generate_text
import db.redb as storage
from serialiser import serialise as s
from inlineapi import respond

router = Router()


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


@router.inline_query()
async def inline_echo(inline_query: types.InlineQuery):
    response = 'Pls enter your request'

    if inline_query.query:
        try:
            response = await respond(inline_query.query)
        except Exception:
            traceback.print_exc()
            response = "Text generation error"

    articles = [types.InlineQueryResultArticle(
            id='text_response',
            title=response,
            input_message_content=types.InputTextMessageContent(message_text='Request: "' + inline_query.query + '"\n\nResponse:\n' + response)
        )]

    await inline_query.answer(articles)
    
