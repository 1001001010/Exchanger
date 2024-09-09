# - *- coding: utf- 8 - *-
import os

import aiofiles
from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery

from bot.data.config import db
from bot.utils.misc.bot_models import FSM, ARS
from bot.utils.const_functions import ded, convert_date

router = Router(name=__name__)

# Открытие профиля 
@router.message(F.text == "👤 Профиль")
async def open_admin_menu(message: Message, bot: Bot, state: FSM, arSession: ARS):
    await state.clear()
    
    user = await db.get_user(user_id=message.from_user.id)
    await message.answer(
        ded(f"""<b>👤 Личный кабинет</b>
            
            👁 Ваш юзернейм: <code>{user['user_name']}</code>
            ⚙️ Id: <code>{user['id']}</code>
            📅 Дара регистрации: <code>{convert_date(user['unix'])}</code>
            
            💱 Обменов: <code>0</code>""")
    )

# Открытие поддержки 
@router.message(F.text == "🚑 Поддержка")
async def open_admin_menu(message: Message, bot: Bot, state: FSM, arSession: ARS):
    await state.clear()
    
    