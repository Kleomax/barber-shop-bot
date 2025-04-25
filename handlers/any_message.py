from aiogram import Router
from aiogram.types import Message

from markups import main_menu

router = Router()


@router.message()
async def any(msg: Message):
    await msg.reply('Не понимаю вас. Пожалуйста, используйте клавиатуру ниже\U0001F447', reply_markup=main_menu.main_menu)