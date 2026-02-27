import asyncio
import logging
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from handlers import basic_handlers, ai_handlers

load_dotenv()
logging.basicConfig(level=logging.INFO)

bot = Bot(token=os.getenv("tgBot_token"))
dp = Dispatcher()

async def main():
    dp.include_router(basic_handlers.router)
    dp.include_router(ai_handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
