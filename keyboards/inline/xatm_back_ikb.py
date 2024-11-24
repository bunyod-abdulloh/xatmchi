import json

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from loader import db

next_callback = CallbackData('def', 'xatm_id', 'info', 'get', 'user_id')


async def xatm_button(user_id, key):
    user = await db.select_xatmuser(id=user_id)
    xatm_ink = InlineKeyboardMarkup(row_width=4)
    user_two = json.loads(user[2])
    n = user_two[key]
    for e in n:
        xatm_ink.insert(InlineKeyboardButton(text=f"{e} - пора",
                                             callback_data=next_callback.new(xatm_id=key, info=str(e), get="qaytarish",
                                                                             user_id=user_id)))
    return xatm_ink
