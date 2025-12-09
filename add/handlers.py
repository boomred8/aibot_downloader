from aiogram import Router, F, types
from aiogram.filters import Command

import add.keyboard as keyboard

router = Router()
dm = False

@router.message(Command('start'))
async def start(message: types.Message):
    await message.answer(f'Hello <b>{message.from_user.username}</b>', parse_mode='html', reply_markup=keyboard.main)

@router.message(F.text.casefold() == 'user_info')
async def user_ifo(message: types.Message):
    await message.answer(f"Information about u:\n"
                         f" username: {message.from_user.username}\n"
                         f" user_id: {message.from_user.id}\n"
                         f" user_language_code: {message.from_user.language_code}", reply_markup=keyboard.main)

@router.message(F.text.lower() == 'download_file')
async def download(message: types.Message):
    global dm
    await message.answer("Ты включил функцию download, что бы выйти напиши команду <b>/stop</b>", parse_mode='html', reply_markup=keyboard.inline_markup())
    dm = True

@router.callback_query(F.data == 'stop')
async def stop_download_callback(callback: types.CallbackQuery):
    global dm
    dm = False
    await callback.answer("Download выключен")
    await callback.message.answer("Ты вышул из режима download",
                          reply_markup=keyboard.main)


@router.message(F.photo | F.voice | F.document)
async def download_file(message: types.Message):
    if not dm:
        return
    bot = message.bot

    if message.photo:
        photo_id = message.photo[-1].file_id
        photo_info = await bot.get_file(photo_id)

        ext = photo_info.file_path.split('.')[-1] # .png, jpg
        save_path = f"./img/{message.from_user.id}.{ext}"

        await bot.download_file(photo_info.file_path, save_path)
        await message.answer("📸 Фото сохранено!")
        return
    elif message.document:
        document_id = message.document.file_id
        document_info = await bot.get_file(document_id)

        document_name = message.document.file_name
        save_path = f"./document/{document_name}"

        await bot.download_file(document_info.file_path, save_path)
        await message.answer("📄 Документ сохранён!")
        return
    elif message.voice:
        voice_id = message.voice.file_id
        voice_info = await bot.get_file(voice_id)

        save_path = f"./voice_user/{message.from_user.id}.ogg"

        await bot.download_file(voice_info.file_path, save_path)
        await message.answer("📄 Документ сохранён!")
        return




