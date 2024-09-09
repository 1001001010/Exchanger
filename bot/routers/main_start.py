# - *- coding: utf- 8 - *-
from aiogram import Router, Bot, F
from aiogram.filters import Command
from aiogram.types import Message

from bot.utils.const_functions import ded
from bot.utils.misc.bot_models import FSM, ARS
from bot.keyboards.reply_main import menu_rep

router = Router(name=__name__)

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