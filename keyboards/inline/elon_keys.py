from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

yes_no = InlineKeyboardMarkup(
    row_width=2,
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="✅  Ҳа",
                callback_data="yes"
            ),
            InlineKeyboardButton(
                text="♻  Йўқ қайтиш",
                callback_data="no_again"
            )
        ]
    ]
)