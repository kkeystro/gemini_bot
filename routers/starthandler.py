from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

import db.redb as storage
from fucked_state_machine import UserStates
from keys.checker import check_key
from keys.requests import add_api_key

router = Router()


@router.message(Command("start"))
async def add_key_1(message: Message, state: FSMContext):
    await storage.delkey(key=str(message.from_user.id))
    await storage.unlock(str(message.from_user.id))
    await message.answer(
        'Отправьте ключ, <a href="https://aistudio.google.com/app/apikey"> получить ключ</a>',
    )
    await state.set_state(UserStates.adding_key)


@router.message(UserStates.adding_key)
async def add_key_2(message: Message, state=FSMContext):
    if await check_key(message.text):
        await add_api_key(message.text)
        await message.answer(
            "Ключ добавлен, добро пожаловать в мир генеративного ИИ!",
            await state.set_state(UserStates.user_not_premium)
        )
    else:
        await message.answer("Ключ недействителен, попробуйте снова")
