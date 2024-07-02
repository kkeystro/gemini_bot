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
async def cmd_start(message: Message, state: FSMContext):
    await storage.delkey(key=str(message.from_user.id))
    await storage.unlock(str(message.from_user.id))
    await message.answer(
        text="Добавьте ключ API",
    )
    await state.set_state(UserStates.choosing_not_to_pay)


@router.message(UserStates.choosing_not_to_pay)
async def add_key_1(message: Message, state: FSMContext):
    await state.update_data(chosen_way=message.text.lower())
    await message.answer(
        "Отправьте ключ, получить ключ можно по ссылке:https://aistudio.google.com/app/prompts/new_chat",
    )
    await state.set_state(UserStates.adding_key)


@router.message(UserStates.adding_key)
async def add_key_2(message: Message, state=FSMContext):
    if await check_key(message.text):
        await add_api_key(message.text)
        await message.answer(
            "Ключ добавлен",
            await state.set_state(UserStates.user_not_premium)
        )
    else:
        await message.answer("Ключ недействителен, попробуйте снова")
