# - *- coding: utf- 8 - *-
import os

import aiofiles
from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery

from bot.data.config import db
from bot.utils.misc.bot_models import FSM, ARS
from bot.utils.const_functions import ded, convert_date
from bot.keyboards.inline_user import support_url_inl

router = Router(name=__name__)

# Открытие профиля 
@router.message(F.text == "👤 Профиль")
async def open_admin_menu(message: Message, bot: Bot, state: FSM, arSession: ARS):
    await state.clear()
    
    user = await db.get_user(user_id=message.from_user.id)
    await message.answer(
        ded(f"""<b>👤 Личный кабинет</b>
            
            👁 Ваш юзернейм: <code>{user['user_name']}</code>
            ⚙️ Id: <code>{user['user_id']}</code>
            📅 Дара регистрации: <code>{convert_date(user['unix'])}</code>
            
            💱 Обменов: <code>0</code>""")
    )

# Открытие информации 
@router.message(F.text == "📝 Информация")
async def open_admin_menu(message: Message, bot: Bot, state: FSM, arSession: ARS):
    await state.clear()
    
    settings = await db.get_settings(id=1)
    await message.answer(settings['info'])
    
# Открытие поддержки 
@router.message(F.text == "🚑 Поддержка")
async def open_admin_menu(message: Message, bot: Bot, state: FSM, arSession: ARS):
    await state.clear()
    
    settings = await db.get_settings(id=1)
    await message.answer("По любым вопросам обращайтесь к нашему саппорту", reply_markup=support_url_inl(settings['support']))