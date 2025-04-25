from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from database.requests import set_user, update_user

from states import reg_state

from markups.send_phone_number import send_phone
from markups.main_menu import main_menu

router = Router()

@router.message(F.text == '/start')
async def start(msg: Message, state: FSMContext):
    user = await set_user(msg.from_user.id)

    print('2', user)
    if not user:
        await msg.answer(f'Добро пожаловать {msg.from_user.first_name}! Пожалуйста, пройдите регистрацию\n\nВведите ваше имя')
        await state.set_state(reg_state.Reg.name)
    else:
        await msg.answer('Вы уже зарегистрированы', reply_markup=main_menu)
        await state.clear()

@router.message(reg_state.Reg.name)
async def get_user_name(msg: Message, state: FSMContext):
    await state.update_data(name = msg.text)

    await msg.answer('Отправьте ваш номер телефона', reply_markup=send_phone)
    await state.set_state(reg_state.Reg.phone_number)
    
@router.message(reg_state.Reg.phone_number, F.contact)
async def get_user_number(msg: Message, state: FSMContext):
    data = await state.get_data()
    await update_user(msg.from_user.id, data['name'], msg.contact.phone_number)

    await msg.answer('Вы успешно зарегистрировались!', reply_markup=main_menu)
    await state.clear()