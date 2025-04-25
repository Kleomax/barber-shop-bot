from aiogram.fsm.state import StatesGroup, State

class Reserve(StatesGroup):
    barber = State()
    time = State()
    service = State()