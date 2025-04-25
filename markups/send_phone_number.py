from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

send_phone = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Отправить номер', request_contact=True)]
    ],
    
    resize_keyboard=True,
    input_field_placeholder='Нажмите кнопку ниже'
)