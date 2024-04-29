from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, ReplyKeyboardRemove
import db.redb as storage
from aiogram.fsm.context import FSMContext
from fucked_state_machine import UserStates
from keyboards.keyboard import make_row_keyboard
from keyboards.buttons import start
from keys.requests import add_api_key
from keys.checker import check_key
from premium.requests import check_premium, add_user

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    await storage.delkey(key=str(message.from_user.id))
    await storage.unlock(str(message.from_user.id))
    try:
        await add_user(message.from_user.id)
        await message.answer(
            text="Добавьте ключ API или воспользуйтесь /premium",
            reply_markup=make_row_keyboard(start)
        )
        await state.set_state(UserStates.choosing_not_to_pay)
    except Exception:
        if await check_premium(message.from_user.id):
            await message.answer("Добро пожаловать в мир LLM")
            await state.set_state(UserStates.user_premium)
        else:
            await message.answer(
                text="Добавьте ключ API или воспользуйтесь /premium",
                reply_markup=make_row_keyboard(start)
            )
            await state.set_state(UserStates.choosing_not_to_pay)


@router.message(UserStates.choosing_not_to_pay)
async def add_key_1(message: Message, state: FSMContext):
    await state.update_data(chosen_way=message.text.lower())
    await message.answer(
        "Отправьте ключ, получить ключ можно по ссылке:https://aistudio.google.com/app/prompts/new_chat",
        reply_markup=ReplyKeyboardRemove()
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
        await message.answer("Ключ недействителен, попробуйте снова или воспользуйтесь /premium")
