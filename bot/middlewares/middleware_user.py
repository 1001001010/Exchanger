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
            get_user = db.get_user(user_id=this_user.id)

            user_id = this_user.id
            user_login = this_user.username
            user_name = clear_html(this_user.first_name)
            user_first_name = clear_html(this_user.first_name)
            user_fullname = clear_html(this_user.first_name)
            user_language = this_user.language_code

            if user_login is None: user_login = ""
            if user_name is None: user_name = ""
            if user_first_name is None: user_first_name = ""
            if user_fullname is None: user_fullname = ""
            if user_language != "ru": user_language = "en"

            if get_user is None:
                db.register_user(user_id, user_name, user_first_name)
            else:
                if user_name != get_user.user_name:
                    db.update_user(get_user.user_id, user_name=user_name)

                if user_first_name != get_user.user_first_name:
                    db.update_user(get_user.user_id, user_first_name=user_first_name)

            data['User'] =  db.get_user(user_id=user_id)

        return await handler(event, data)