import json

import asyncpg
from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.default.start_dk import main_keyboard
from keyboards.default.xatm_default_key import menu
from loader import dp, db

XATM_ADMINS = [1041847396]


@dp.message_handler(text="🎙 Онлайн хатм", state="*")
async def onlayn_xatm_func(msg: types.Message):
    await msg.answer("Хатмонага марҳабо!",
                     reply_markup=menu)

    try:
        await db.add_xatmuser(
            id=msg.from_user.id,
            full_name=msg.from_user.full_name,
            poralar="{}"
        )
    except asyncpg.exceptions.UniqueViolationError:
        pass
    user = await db.select_xatmuser(id=msg.from_user.id)

    if user[2] != "{}":
        user1 = json.loads(user[2])
        await msg.answer("Сизга аввал берилган поралар:")
        x1 = 0
        p1 = 0
        for k, v in user1.items():
            if len(v) == 0:
                pass
            else:
                if len(v) == 1:
                    p1 += len(v)
                    await msg.answer(f"\n\n{k} - хатмдан: \n<b>{v}</b> - пора")
                else:
                    p1 += len(v)
                    await msg.answer(f"\n\n{k} - хатмдан: \n<b>{v}</b> - поралар")
                x1 += 1
        await msg.answer(f"Сизга жами {x1} та хатмдан {p1} пора берилган!")


@dp.message_handler(text="⬅️ Ortga", state="*")
async def back_to_main(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(
        text=message.text, reply_markup=main_keyboard
    )
