# - *- coding: utf- 8 - *-
from aiogram import Router, Bot, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from bot.data.config import db
from bot.utils.const_functions import ded
from bot.utils.misc.bot_models import FSM, ARS
from bot.keyboards.reply_main import menu_rep
from bot.keyboards.inline_user import support_url_inl
from bot.utils.misc.bot_filters import IsWork

router = Router(name=__name__)

# Фильтр на технические работы - сообщение
@router.message(IsWork())   
async def filter_work_message(message: Message, bot: Bot, state: FSM, arSession: ARS):
    await state.clear()

    get_settings = await db.get_settings(id=1)

    if get_settings['support'] != "":
        return await message.answer(
            "<b>⛔ Бот находится на технических работах.</b>",
            reply_markup=support_url_inl(get_settings['support']),
        )

    await message.answer("<b>⛔ Бот находится на технических работах.</b>")


# Фильтр на технические работы - колбэк
@router.callback_query(IsWork())
async def filter_work_callback(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS):
    await state.clear()

    await call.answer("⛔ Бот находится на технических работах.", True)

# Открытие главного меню
@router.message(F.text.in_(('🔙 Главное меню', '🔙 Назад')))
@router.message(Command(commands=['start']))
async def main_start(message: Message, bot: Bot, state: FSM, arSession: ARS):
    await state.clear()

    await message.answer(
        ded(f"""<b>Добро пожаловать в наш обменник</b>
            
            Воспользуйтесь меню нижу"""), 
        reply_markup=menu_rep(user_id=message.from_user.id)
    )