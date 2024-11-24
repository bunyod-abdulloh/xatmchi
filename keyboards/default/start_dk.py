from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("🎙 Онлайн хатм"),
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
