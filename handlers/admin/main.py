import json

from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import ADMINS
from handlers.admin.functions import statistika_func, sarhisob_func
from keyboards.default.xatm_default_key import xatm_adminka
from keyboards.inline.elon_keys import yes_no
from loader import dp, db


@dp.message_handler(text=['/admin'], user_id=ADMINS, state='*')
async def xatm_admin_func(msg: types.Message):
    await msg.answer("Хатм админлари учун тугмалар", reply_markup=xatm_adminka)
    xatmona = await db.select_users_stat(id=0)
    if xatmona[2] == 1:
        await msg.answer(f"Хатм учун поралар олиш ҳолати: Очиқ")
    else:
        await msg.answer(f"Хатм учун поралар олиш ҳолати: Ёпиқ")


@dp.message_handler(text="🔓 Хатм вақтини очиш", user_id=ADMINS, state="*")
async def ochish_func(msg: types.Message):
    await db.update_stat_users_poralar(1, 0)
    await msg.answer("Хатм учун поралар тарқатиш вақти очилди")


@dp.message_handler(text="🔒 Хатм вақтини ёпиш", user_id=ADMINS, state="*")
async def yopish_func(msg: types.Message):
    await db.update_stat_users_poralar(0, 0)
    await msg.answer("Хатм учун поралар тарқатиш вақти ёпилди")


@dp.message_handler(text="📊 Жорий ҳолат", user_id=ADMINS)
async def bot_start(msg: types.Message):
    await statistika_func(msg)


@dp.message_handler(text="🧮 Сарҳисоб", state="*", user_id=ADMINS)
async def bot_start(msg: types.Message, state: FSMContext):
    await msg.answer("Хатмонани якунлашни истайсизми? Илтимос эътибор қилинг, \"✅ Ҳа\" "
                     "тугмасини боссангиз хатмона жадвали ёпилади. Бу тугмани иложи борича хатмоналар жамланиб"
                     " бағишланганидан сўнг босиш тавсия этилади",
                     reply_markup=yes_no)
    await state.set_state("sarhisob")


@dp.callback_query_handler(state="sarhisob")
async def backporalar(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    if call.data == "yes":
        all_xt = await db.select_all_xatms()
        all_us = await db.select_xatmdagi_user(poralar="{}")

        await sarhisob_func(call.message)

        for a in all_us:
            source = json.loads(a[2])
            xatms = 1
            poralar = 0

            for key, value in source.items():
                poralar += len(value)

            us_stat = await db.select_users_stat(id=a[0])

            if not us_stat:
                await db.add_users_stat(a[0], a[1], poralar, xatms)
            else:
                xatms = us_stat[3] + xatms
                poralar = us_stat[2] + poralar
                await db.update_stat_users_xatms(xatms, a[0])
                await db.update_stat_users_poralar(poralar, a[0])
            await db.update_user_poralar("{}", a[0])
        for n in all_xt:
            if n[1] == "[]":
                await db.delete_xatm(n[0])
            else:
                await db.update_user_xatm_data("{}", n[0])

        all_ = await db.select_all_xatms()
        if not all_:
            list1 = [n for n in range(1, 31)]
            await db.add_xatm_db(id=all_xt[-1][0] + 1, list=json.dumps(list1), xatm_data="{}")

    else:
        await call.message.answer("Керакли бўлимни танлашингиз мумкин", reply_markup=xatm_adminka)

    await state.finish()
