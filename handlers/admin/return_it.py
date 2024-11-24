from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import ADMINS
from handlers.users.functions import qaytarish_functions, fback
from keyboards.inline.xatm_back_ikb import next_callback, xatm_button
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
        await state.set_state("get_qaytarish")
        # await state.update_data(user_id=user_id)
    else:
        await msg.answer("Фойдаланувчи ID рақамини киритинг: ")
        await state.set_state("qaytarish_admin")


@dp.callback_query_handler(next_callback.filter(get='qaytarish'), state="get_qaytarish")
async def backporalar(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    # statedan = await state.get_data()
    user_id = int(callback_data['user_id'])
    list1 = callback_data['info']
    list2 = [int(list1)]
    xatm_id = callback_data['xatm_id']

    await fback(user_id=user_id, list_xatm=list2, xatm_id=xatm_id)
    await call.message.edit_reply_markup(reply_markup=await xatm_button(user_id=user_id, key=xatm_id))

    await call.answer(text=f"{user_id} фойдаланувчидан {list1} - пора қайтариб олинди!", show_alert=True)
    await state.finish()
