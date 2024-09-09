# - *- coding: utf- 8 - *-
from aiogram import Router, Bot, F
from aiogram.filters import Command
from aiogram.types import Message

from bot.utils.const_functions import ded
from bot.utils.misc.bot_models import FSM, ARS

router = Router(name=__name__)

# Открытие главного меню
@router.message(F.text.in_(('🔙 Главное меню', '🔙 Назад')))
@router.message(Command(commands=['start']))
async def main_start(message: Message, bot: Bot, state: FSM, arSession: ARS):
    await state.clear()

    await message.answer(
        ded(f"""
            🔸 Hello
            🔸 Enter /start or /inline
        """)
    )