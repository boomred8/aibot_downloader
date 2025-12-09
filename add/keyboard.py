from aiogram.types import KeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardButton, ReplyKeyboardBuilder, InlineKeyboardBuilder

main = ReplyKeyboardBuilder()
main.add(
    KeyboardButton(text='/start'),
    KeyboardButton(text='user_info'),
    KeyboardButton(text='download_file')
)
main = main.adjust(2).as_markup(
    resize_keyboard=True,
    input_field_placeholder='выбери команду'
)

#stop_markup = InlineKeyboardMarkup(inline_keyboard=[
#    [InlineKeyboardButton(text='stop to download', callback_data='stop')]
#])

def inline_markup() -> InlineKeyboardMarkup:
    stop_markup = InlineKeyboardBuilder()
    stop_markup.add(
        InlineKeyboardButton(text='stop to download', callback_data='stop')
    )
    return stop_markup.as_markup()

