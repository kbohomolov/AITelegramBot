import os
import asyncio
import logging

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, BaseMiddleware
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.utils.i18n import I18n
from aiogram.utils.i18n.middleware import SimpleI18nMiddleware

from app.handlers.user import user_router
from app.handlers.admin import admin_router
from app.database.models import async_main
import app.database.requests as rq


class DbLanguageMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        user = await rq.get_user(event.from_user.id)
        lang = user.language if user else "uk"
        data["locale"] = lang
        return await handler(event, data)


async def main():
    load_dotenv()
    await async_main()
    bot = Bot(
        token=os.getenv("TOKEN"),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()

    i18n = I18n(path="app/locales", default_locale="uk", domain="messages")
    dp.message.middleware(DbLanguageMiddleware())
    dp.callback_query.middleware(DbLanguageMiddleware())
    dp.message.middleware(SimpleI18nMiddleware(i18n))
    dp.callback_query.middleware(SimpleI18nMiddleware(i18n))

    dp.include_router(user_router)
    dp.include_router(admin_router)

    logging.info("Бот успішно запущено!")
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот вимкнено!")