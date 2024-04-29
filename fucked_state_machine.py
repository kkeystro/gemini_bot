from aiogram.fsm.state import StatesGroup, State


class UserStates(StatesGroup):
    choosing_not_to_pay = State()
    adding_key = State()
    user_not_premium = State()
    user_premium = State()
