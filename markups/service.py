from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.requests import get_barbers, get_services, get_barber_time, get_reserve

async def barbers():
    barbers_name = InlineKeyboardBuilder()

    all_barbers = await get_barbers()

    for barber in all_barbers:
        barbers_name.add(InlineKeyboardButton(text=barber.barber_name, callback_data=f'barber_{barber.barber_name}'))

    barbers_name.row(InlineKeyboardButton(text='\U000021A9 Назад', callback_data='backBtn'))

    return barbers_name.adjust(1).as_markup()

async def services():
    services = InlineKeyboardBuilder()

    all_services = await get_services()

    for service in all_services:
        services.add(InlineKeyboardButton(
            text=service.name, callback_data=f'service_{service.name}'))

    services.row(InlineKeyboardButton(
        text='\U000021A9 Назад', callback_data='backBtn'))

    return services.adjust(1).as_markup()


async def time(barber_name):
    times = InlineKeyboardBuilder()

    all_time = await get_barber_time(barber_name)
    all_reserve = await get_reserve()

    reservations_time = []
    for reserve in all_reserve:
        reservations_time.append(reserve.time)

    for time in all_time:
        time = time.barber_time.split(',')
        for i in time:
            if i in reservations_time:
                times.add(InlineKeyboardButton(text=f"{i} (Занято)", callback_data=f'occupied'))
            else:
                times.add(InlineKeyboardButton(text=i, callback_data=f'{i}'))

    times.row(InlineKeyboardButton(
        text='\U000021A9 Назад', callback_data='backBtn'))
    

    return times.adjust(1).as_markup()