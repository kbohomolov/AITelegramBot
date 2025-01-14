import os
import asyncio
import logging

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher

from app.handlers.user import user_router
from app.handlers.admin import admin_router
from app.database.models import async_main


async def main():
    load_dotenv()
    bot = Bot(token=os.getenv('TOKEN'))
    dp = Dispatcher()
    dp.include_routers(user_router, admin_router)
    await async_main()
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try: 
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот вимкнено!')
  