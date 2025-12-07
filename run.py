import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command

from main import bot_token, download_message

bot = Bot(token=bot_token)
dp = Dispatcher()

dm = download_message

# создаём папки, если их нет
os.makedirs('document', exist_ok=True)
os.makedirs('img', exist_ok=True)
os.makedirs('voice_user', exist_ok=True)


@dp.message(Command('start'))
async def start(message: types.Message):
    await message.answer(
        f"Hello <b>{message.from_user.username}</b>",
        parse_mode='html'
    )


@dp.message(Command('download'))
async def cmd_download(message: types.Message):
    global dm
    dm = True
    await message.answer(
        "Можешь скидывать документ, фото или голосовое.\n"
        "Если хочешь выйти — используй /stop"
    )


@dp.message(Command('stop'))
async def cmd_stop(message: types.Message):
    global dm
    dm = False
    await message.answer("Ты вышел")


@dp.message(F.photo | F.voice | F.document)
async def download(message: types.Message):
    if not dm:
        return

    # Фото
    if message.photo:
        photo_id = message.photo[-1].file_id
        photo_info = await bot.get_file(photo_id)

        ext = photo_info.file_path.split('.')[-1]
        save_path = f"./img/{message.from_user.id}.{ext}"

        await bot.download_file(photo_info.file_path, save_path)
        await message.answer("📸 Фото сохранено!")
        return

    # Голосовые
    if message.voice:
        voice_id = message.voice.file_id
        voice_info = await bot.get_file(voice_id)

        voice_name = f"voice_{message.from_user.id}.ogg"
        save_path = f"./voice_user/{voice_name}"

        await bot.download_file(voice_info.file_path, save_path)
        await message.answer("🎤 Голос сохранён!")
        return

    # Документы
    if message.document:
        document_id = message.document.file_id
        document_info = await bot.get_file(document_id)

        document_name = message.document.file_name
        save_path = f"./document/{document_name}"

        await bot.download_file(document_info.file_path, save_path)
        await message.answer("📄 Документ сохранён!")
        return


async def main():
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