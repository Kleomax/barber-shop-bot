from aiogram.fsm.state import StatesGroup, State

class Reg(StatesGroup):
    name = State()
    phone_number = State()