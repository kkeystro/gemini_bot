from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, ReplyKeyboardRemove
import db.redb as storage
from aiogram.fsm.context import FSMContext
from fucked_state_machine import UserStates
from premium.requests import check_premium, set_premium

router = Router()


@router.message(Command("clear"))
async def cmd_clear(message: Message):
    await storage.delkey(key=str(message.from_user.id))
    await message.answer(
        "Hystory cleared",
    )


@router.message(Command('premium'))
async def get_premium(message: Message, state: FSMContext):
    if await check_premium(message.from_user.id):
        await message.answer("Вы уже занесли", reply_markup=ReplyKeyboardRemove())
        await state.set_state(UserStates.user_premium)
    else:
        await set_premium(message.from_user.id)
        await message.answer("Теперь вы мощный", reply_markup=ReplyKeyboardRemove())
        await state.set_state(UserStates.user_premium)
