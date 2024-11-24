import json

from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.xatm_back_ikb import next_callback
from loader import db


async def pora_biriktirish(xatm_id: int, user_id: int, poralar: list, info_xatm: str):
    user = await db.select_xatmuser(id=user_id)

    info_xatm = json.loads(info_xatm)
    info_user = json.loads(user[2])
    if str(user_id) in info_xatm.keys():
        info_xatm[str(user_id)].extend(poralar)
        info_user[str(xatm_id)].extend(poralar)
    else:
        info_xatm[str(user_id)] = poralar
        info_user[str(xatm_id)] = poralar
    await db.update_user_xatm_data(json.dumps(info_xatm), xatm_id)  #
    await db.update_user_poralar(json.dumps(info_user), user_id)


async def pora_ajratish(user_id: int, poralar: list, get_from_xatm: int, key):
    user = await db.select_xatmuser(id=user_id)
    info_user = json.loads(user[2])
    for n in poralar:
        value = info_user[key]
        if n in value:
            info_user[key].remove(n)

            a = await db.select_user_xatms(id=int(key))
            d = json.loads(a[2])
            d[str(user_id)].remove(n)

            if key != str(get_from_xatm):
                second_xatm = await db.select_user_xatms(id=get_from_xatm)
                dict_x = json.loads(second_xatm[2])
                for k, v in dict_x.items():
                    if n in v:

                        dict_x[k].remove(n)
                        u = await db.select_xatmuser(id=int(k))
                        dict_u = json.loads(u[2])
                        dict_u[str(get_from_xatm)].remove(n)

                        if key in dict_u.keys():
                            dict_u[key].extend(poralar)
                        else:
                            dict_u[key] = poralar

                        dict_u[key].sort()
                        await db.update_user_poralar(json.dumps(dict_u), int(k))
                        await db.update_user_xatm_data(json.dumps(dict_x), get_from_xatm)
                        if k in d.keys():
                            d[k].extend(poralar)
                        else:
                            d[k] = poralar
                        d[k].sort()
            await db.update_user_xatm_data(json.dumps(d), int(key))
            await db.update_user_poralar(json.dumps(info_user), user_id)
            break


async def fback(user_id, xatm_id, list_xatm):
    all_xatm = await db.select_all_xatms()
    l_xatm = list_xatm[:]

    for i in range(1, len(all_xatm) + 1):
        last = json.loads(all_xatm[-i][1])
        if not list_xatm[0] in last:
            last.append(list_xatm[0])
            list_xatm.pop(0)
        last.sort()
        await pora_ajratish(user_id, l_xatm, all_xatm[-i][0], xatm_id)

        await db.update_user_xatm_list(json.dumps(last), all_xatm[-i][0])

        if not list_xatm:
            break


async def qaytarish_functions(message: types.Message, user_id, text):
    user = await db.select_xatmuser(id=user_id)
    user_two = json.loads(user[2])

    if user[2] == "{}":
        await message.answer(text=text)
    else:
        for key, n in user_two.items():
            if len(n) == 0:
                pass
            else:
                xatm_ink = InlineKeyboardMarkup(row_width=4)
                for e in n:
                    xatm_ink.insert(InlineKeyboardButton(text=f"{e} - пора",
                                                         callback_data=next_callback.new(xatm_id=key, info=str(e),
                                                                                         get="qaytarish",
                                                                                         user_id=user_id)))
                await message.answer(f"{key} - хатмдан қайтариладиган поралар тартиб рақамини танланг: ",
                                     reply_markup=xatm_ink)
