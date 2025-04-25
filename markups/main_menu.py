from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Выбрать услугу')],
        [KeyboardButton(text='Контакты/Локация')]
    ],

    resize_keyboard=True,
)
