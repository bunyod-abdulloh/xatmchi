import json

from aiogram import types

from loader import dp, db


@dp.message_handler(text="👤 ID олиш", state="*")
async def idqaytar(msg: types.Message):
    sel = await db.select_xatmuser(id=msg.from_user.id)
    select = json.loads(sel[2])
    if len(select) == 0:
        await msg.answer(f"Сизнинг ID рақамингиз: \n\n<b><code>{msg.from_user.id}</code></b>")
    else:
        await msg.answer("Сизга берилган поралар:")
        x1 = 0
        p1 = 0
        for k, v in select.items():
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

        await msg.answer(f"Сизнинг ID рақамингиз: \n\n<b><code>{msg.from_user.id}</code></b>")
