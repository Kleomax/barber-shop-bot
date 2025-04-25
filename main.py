from database.requests import delete_reserve
from handlers import any_message, start_msg, choose_service
from config import BOT_TOKEN
import asyncio
import logging
from aiogram import Dispatcher, Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler

import datetime

import multiprocessing

# from database.models import create_tables
# from database.requests import get_barber_time
dp = Dispatcher()


async def scheduler():
    time = {
        "8:00": [],
        "20:00": [],
        "08.08": [],
        "07.08": []
    }

    while True:
        if datetime.datetime.now().strftime('%H:%M') in time:
            await delete_reserve()
        await asyncio.sleep(30)


def worker():
    asyncio.run((scheduler()))


async def main():
    # await create_tables()
    process = multiprocessing.Process(target=worker)
    process.start()
    bot = Bot(token=BOT_TOKEN)
    dp.include_routers(
        start_msg.router,
        choose_service.router,
        any_message.router
    )

    # logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

    process.join()

if __name__ == '__main__':
    try:
        logging.basicConfig(level=logging.INFO)
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот остановлен')
