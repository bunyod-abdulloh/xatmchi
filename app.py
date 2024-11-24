import json
import middlewares, filters, handlers

from aiogram import executor

from loader import dp, db, bot
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    await db.create()
    # await db.drop_xatmusers()
    # await db.drop_table_xatm_db()
    # await db.drop_table_users_stat()

    await db.create_table_stat()
    await db.create_table_xatmusers()
    await db.create_table_xatm_db()

    list1 = [n for n in range(1, 31)]
    await db.add_xatm_db(id=1, list=json.dumps(list1), xatm_data="{}")
    await db.add_users_stat(0, "Poralar taqsimlash holati", 1, 1)
    await bot.delete_my_commands()
    await set_default_commands(dispatcher)

    await on_startup_notify(dispatcher)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
