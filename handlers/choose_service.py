from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from database.requests import set_user, update_user, get_barbers, set_reserve, delete_reserve, get_reserve, check_reserve

from states import reg_state, reserve_state

from markups.send_phone_number import send_phone
from markups.main_menu import main_menu
from markups.service import barbers, services, time

router = Router()


@router.message(F.text == 'Выбрать услугу')
async def choose_service(msg: Message, state: FSMContext):
    all_reserve = await check_reserve(msg.from_user.id)



    # if all_reserve:

    #     await msg.answer(f'Вы уже записаны на \n\nстрижку {user_info[2]}\nк мастеру {user_info[1]}\nНа время: {user_info[]}')
    await msg.answer('Выберите мастера', reply_markup = await barbers())
    await state.set_state(reserve_state.Reserve.barber)

@router.callback_query(reserve_state.Reserve.barber)
async def choose_barber(call: CallbackQuery, state: FSMContext):
    if call.data == 'backBtn':
        await call.message.answer('Вы вернулись в главное меню', reply_markup=main_menu)
        await state.clear()
    else:
        await state.update_data(barber = call.data)
        await state.set_state(reserve_state.Reserve.service)

        await call.message.answer('Выберите услугу', reply_markup = await services())

@router.callback_query(reserve_state.Reserve.service)
async def choose_barber(call: CallbackQuery, state: FSMContext):
    if call.data == 'backBtn':
        await call.message.answer('Выберите мастера', reply_markup=await barbers())
        await state.set_state(reserve_state.Reserve.barber)
    else:
        data = await state.get_data()
        barber_id = data['barber'].split('_')
        await state.update_data(service=call.data)
        await state.set_state(reserve_state.Reserve.time)


    # await call.message.answer('К сожалению у данного мастера всё время занято')

    await call.message.answer('Выберите время', reply_markup = await time(barber_id[1]))

@router.callback_query(reserve_state.Reserve.time)
async def choose_time(call: CallbackQuery, state: FSMContext):
    if call.data == 'backBtn':
        await call.message.answer('Выберите услугу', reply_markup= await services())
        await state.set_state(reserve_state.Reserve.service)

    elif call.data == 'occupied':
        await call.message.answer('Данное время занято. Пожалуйста, выберите другое время')
    
    else:
        data = await state.get_data()

        barber = data['barber'].split('_')
        service = data['service'].split('_')
        print(barber[1])
        await set_reserve(int(call.from_user.id), barber[1], service[1], call.data)

        await call.message.answer(f'Вы успешно записались на {call.data}', reply_markup=main_menu)

        await state.clear()

@router.message(F.text == 'd')
async def dela(msg: Message):
    await delete_reserve()
    await msg.answer('U')