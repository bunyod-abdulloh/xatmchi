from aiogram import types

from loader import dp


@dp.message_handler(text="📖 Қоида ва йўриқнома", state="*")
async def yuriqnoma_func(msg: types.Message):
    await msg.answer("Онлайн хатмда иштирок этиш бўйича йўриқнома. \n\nhttps://telegra.ph/Onlayn-xatm-11-20")
