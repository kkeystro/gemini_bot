from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
import db.redb as storage
from aiogram.fsm.context import FSMContext
from fucked_state_machine import UserStates
from premium.requests import check_premium, set_premium
from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardBuilder
from connector import get_connector
import asyncio
from pytoniq_core import Address
from keyboards import inline_buttons
from pytonconnect import TonConnect

router = Router()


@router.message(Command("clear"))
async def cmd_clear(message: Message):
    await storage.delkey(key=str(message.from_user.id))
    await message.answer(
        "Hystory cleared",
    )


async def connect_wallet(message: Message, wallet_name: str):
    connector = get_connector(message.chat.id)

    wallets_list = connector.get_wallets()
    wallet = None

    for w in wallets_list:
        if w['name'] == wallet_name:
            wallet = w

    if wallet is None:
        raise Exception(f'Unknown wallet: {wallet_name}')

    generated_url = await connector.connect(wallet)

    mk_b = InlineKeyboardBuilder()
    mk_b.button(text='Connect', url=generated_url)

    await message.answer('Connect wallet within 3 minutes', reply_markup=mk_b.as_markup())

    mk_b = InlineKeyboardBuilder()
    mk_b.button(text='Start', callback_data='start')

    for i in range(1, 180):
        await asyncio.sleep(1)
        if connector.connected:
            if connector.account.address:
                wallet_address = connector.account.address
                wallet_address = Address(wallet_address).to_str(is_bounceable=False)
                await message.answer(f'You are connected with address <code>{wallet_address}</code>',
                                     reply_markup=inline_buttons.get_connected())
            return

    await message.answer(f'Timeout error!', reply_markup=mk_b.as_markup())


@router.message(Command('premium'))
async def get_premium(message: Message, state: FSMContext):
    chat_id = message.chat.id
    connector = get_connector(chat_id)
    connected = await connector.restore_connection()
    if await check_premium(message.from_user.id):
        await message.answer("Вы уже занесли", reply_markup=ReplyKeyboardRemove())
        await state.set_state(UserStates.user_premium)
    else:
        if connected:
            await message.answer("Пожалуйста, оплатите premium", reply_markup=inline_buttons.get_connected())
        else:
            await message.answer("Подключите кошелёк", reply_markup=inline_buttons.get_base())


@router.callback_query(F.data == 'connecting_wallet')
async def wallet_connect(call: CallbackQuery):
    mk_b = InlineKeyboardBuilder()
    wallets_list = TonConnect.get_wallets()
    for wallet in wallets_list:
        mk_b.button(text=wallet['name'], callback_data=f'connect:{wallet["name"]}')
    mk_b.adjust(1, )
    await call.message.edit_text(text='Choose wallet to connect', reply_markup=mk_b.as_markup())


@router.callback_query(lambda call: True)
async def main_callback_handler(call: CallbackQuery):
    await call.answer()
    message = call.message
    data = call.data
    data = data.split(':')
    if data[0] == 'connect':
        await connect_wallet(message, data[1])
