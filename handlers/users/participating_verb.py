import json

from aiogram import types
from aiogram.dispatcher import FSMContext

from filters.forscheduler import ForXatmona
from handlers.users.functions import pora_biriktirish
from keyboards.inline.elon_keys import yes_no
from loader import dp, db


@dp.message_handler(ForXatmona(), text="✅ Иштирок этиш", state="*")
async def bot_start(msg: types.Message, state: FSMContext):
    await msg.answer(
        "Неча пора ўқимоқчисиз?\n\nИлтимос 1 дан 30 гача бўлган рақамлардан киритинг:")
    await state.set_state("xatm1")


@dp.message_handler(state="xatm1")
async def mashqxatm(msg: types.Message, state: FSMContext):
    if msg.text.isdigit() and int(msg.text) < 31:
        await state.update_data(pora=msg.text)
        await msg.answer(
            "Керакли тугмани босинг",
            reply_markup=yes_no)
        await state.set_state("xatm2")
    else:
        await msg.answer("Илтимос 1 дан 30 гача бўлган рақамлардан киритинг: ")


@dp.callback_query_handler(state="xatm2")
async def bot_starts(call: types.CallbackQuery, state: FSMContext):
    if call.data == "yes":
        data = await state.get_data()
        habar = int(data['pora'])
        list_two = []
        cn = 0

        while True:

            xatms_all = await db.select_all_xatms()
            tr = len(xatms_all)

            xatm_db = xatms_all[cn]

            list_one = json.loads(xatm_db[1])

            if list_one:
                uzunligi = len(list_one)
                rel_list = []
                for n in range(uzunligi):
                    p = list_one.pop(0)
                    rel_list.append(p)
                    list_two.append(p)

                    if len(list_two) == habar:
                        break
                list_one.sort()
                rel_list.sort()
                await db.update_user_xatm_list(json.dumps(list_one), xatm_db[0])
                await pora_biriktirish(xatm_db[0], call.from_user.id, rel_list, xatm_db[2])
                rel_list.clear()

                if len(list_two) == habar:
                    break

                if cn + 1 != tr:
                    cn += 1
                    continue

                list1 = [n for n in range(1, 31)]
                await db.add_xatm_db(id=xatm_db[0] + 1, list=json.dumps(list1), xatm_data="{}")
                list_one = list1[:]
                rel_list = []
                for e in range(len(list_one)):
                    p = list_one.pop(0)
                    rel_list.append(p)
                    list_two.append(p)
                    if len(list_two) == habar:
                        list_one.sort()
                        rel_list.sort()
                        await pora_biriktirish(xatm_db[0] + 1, call.from_user.id, rel_list, "{}")
                        rel_list.clear()

                        await db.update_user_xatm_list(json.dumps(list_one), xatm_db[0] + 1)
                        break
                break

            elif cn + 1 != tr:
                cn += 1

            else:
                list1 = [n for n in range(1, 31)]
                await db.add_xatm_db(id=xatm_db[0] + 1, list=json.dumps(list1), xatm_data="{}")
                cn += 1

        await call.message.delete()

        us = await db.select_xatmuser(id=call.from_user.id)
        user = json.loads(us[2])
        await call.message.answer("Сизгa берилган поралар:")
        x1 = 0
        p1 = 0
        for k, v in user.items():
            if len(v) == 1:
                p1 += len(v)
                await call.message.answer(f"\n\n{k} - хатмдан: \n<b>{v}</b> - пора")
            else:
                p1 += len(v)
                await call.message.answer(f"\n\n{k} - хатмдан: \n<b>{v}</b> - поралар")
            x1 += 1

        if len(list_two) == 1:
            await call.message.answer(f"Сизга жами {x1} та хатмдан {p1} пора берилди!"
                                      )  # f"\n\n{list_two} - пора қўшилди."
        else:
            await call.message.answer(f"Сизга жами {x1} та хатмдан {p1} пора берилди!"
                                      )  # f"\n\n{list_two} - поралар қўшилди."
        await state.finish()

    elif call.data == "no_again":
        await call.message.answer(
            "Неча пора ўқимоқчисиз?\n\nИлтимос 1 дан 30 гача бўлган рақамлардан киритинг: ")
        await state.set_state("xatm1")


@dp.message_handler(text="✅ Иштирок этиш", state="*")
async def bot_start(msg: types.Message):
    await msg.answer("Хатмларни тақсимлаш вақти ёпилган! Қатнашиш истагингиз бўлса, админга мурожаат қилишингиз мумкин")
