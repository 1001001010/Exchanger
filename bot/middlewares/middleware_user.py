# - *- coding: utf- 8 - *-
from aiogram import BaseMiddleware

# from bot.database.db_users import Userx
from bot.data.config import db
from bot.utils.const_functions import clear_html


# Проверка юзера в БД и его добавление
class ExistsUserMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        this_user = data.get("event_from_user")

        if not this_user.is_bot:
            get_user = await db.get_user(user_id=this_user.id)

            user_id = this_user.id
            user_name = clear_html(this_user.first_name)
            user_first_name = clear_html(this_user.first_name)
            
            if user_name is None: user_name = ""
            if user_first_name is None: user_first_name = ""

            if get_user is None:
                await db.register_user(user_id=user_id, user_name=user_name, first_name=user_first_name)
            else:
                if user_name != get_user["user_name"]:
                    await db.update_user(get_user.user_id, user_name=user_name)

                if user_first_name != get_user['first_name']:
                    await db.update_user(get_user.user_id, user_first_name=user_first_name)

            data['User'] =  await db.get_user(user_id=user_id)

        return await handler(event, data)