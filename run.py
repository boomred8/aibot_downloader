import asyncio
import logging
import os

from aiogram import Bot, Dispatcher

from main import bot_token
from add.handlers import router


bot = Bot(token=bot_token)
dp = Dispatcher()

# создаём папки, если их нет
os.makedirs('document', exist_ok=True)
os.makedirs('img', exist_ok=True)
os.makedirs('voice_user', exist_ok=True)

async def main():
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")