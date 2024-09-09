# - *- coding: utf- 8 - *-
from typing import Union

from aiogram import Bot
from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery

from bot.data.config import get_admins, db


# Проверка на админа
class IsAdmin(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if message.from_user.id in get_admins():
            return True
        else:
            return False
        
# Проверка на технические работы
class IsWork(BaseFilter):
    async def __call__(self, update: Union[Message, CallbackQuery], bot: Bot) -> bool:
        get_settings = await db.get_settings(id=1)

        if get_settings['is_work'] == "True" or update.from_user.id in get_admins():
            return False
        else:
            return True