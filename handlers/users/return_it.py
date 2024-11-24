import json

from aiogram import types

from handlers.users.functions import fback, qaytarish_functions
from keyboards.inline.xatm_back_ikb import next_callback, xatm_button
from loader import dp, db


@dp.message_handler(text="♻ Қайтариш", state="*")
async def qaytarish_func(msg: types.Message):
    await qaytarish_functions(
        message=msg, user_id=msg.from_user.id, text="Сиз ҳали хатмонада иштирок этмадингиз!"
    )


@dp.callback_query_handler(next_callback.filter(get='qaytarish'))
async def backporalar_user(call: types.CallbackQuery, callback_data: dict):
    list1 = callback_data['info']
    xatm_id = callback_data['xatm_id']
    list2 = [int(list1)]
    user_id = int(callback_data['user_id'])
    backp = await db.select_xatmuser(id=user_id)
    check = True
    massiv = 0
    json1 = list(json.loads(backp[2]).items())
    json1.reverse()
    for key, value in json1:
        if list2[0] in value and int(key) > int(xatm_id):
            check = False
            massiv = key
            break
    if check:

        await fback(user_id, xatm_id, list2)
        await call.message.edit_reply_markup(reply_markup=await xatm_button(user_id=user_id, key=xatm_id))

        await call.answer(text=f"{xatm_id} - хатмдан {list1} - пора қайтариб олинди!", show_alert=True)
    else:
        await call.answer(f"Ўчириш мумкин эмас! Ушбу порани аввал {massiv} - хатмдан ўчиринг!", show_alert=True)
