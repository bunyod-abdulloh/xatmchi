import asyncpg
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters.builtin import CommandStart
from keyboards.default.start_dk import main_keyboard

from loader import dp, bot

@dp.message_handler(CommandStart(), state="*")
async def bot_start(msg: Message):
    await msg.answer("start",
                     reply_markup=main_keyboard)