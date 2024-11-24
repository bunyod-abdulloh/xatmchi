from loader import db, dp
from aiogram import types
from aiogram.dispatcher.filters import Filter

class ForXatmona(Filter):

    async def check(self, message: types.Message):
        xatmona = await db.select_users_stat(id=0)

        if xatmona[2] == 1:
            return True
        else:
            return False
