from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import ADMINS
from handlers.users.functions import qaytarish_functions
from loader import dp


@dp.message_handler(text="❎ Қайтариш админ", user_id=ADMINS)
async def bot_start(msg: types.Message, state: FSMContext):
    await msg.answer("Қайси фойдаланувчи номидан қайтармоқчисиз? (ID рақамини киритинг): ")
    await state.set_state("qaytarish_admin")


@dp.message_handler(state="qaytarish_admin")
async def bot_start(msg: types.Message, state: FSMContext):
    if msg.text.isdigit():
        user_id = msg.from_user.id
        await qaytarish_functions(
            message=msg, user_id=user_id, text="Foydalanuvchi hali xatmonada ishtirok etmadi!"
        )
        await state.finish()
    else:
        await msg.answer("Фойдаланувчи ID рақамини киритинг: ")
        await state.set_state("qaytarish_admin")
