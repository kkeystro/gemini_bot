from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardMarkup


def get_base():
    base = [[
        InlineKeyboardButton(text="Подключить Кошелёк", callback_data="connecting_wallet")
    ]]
    keyboard = InlineKeyboardMarkup(inline_keyboard=base)
    return keyboard


def get_connected():
    connected = [[
        InlineKeyboardButton(text="Оплатить", callback_data="paying"),
        InlineKeyboardButton(text="Сменить адрес", callback_data="connecting_wallet")
    ]]
    keyboard = InlineKeyboardMarkup(inline_keyboard=connected)
    return keyboard
