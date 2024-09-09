# - *- coding: utf- 8 - *-
from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from bot.data.config import get_admins
from bot.utils.const_functions import rkb


# Кнопки главного меню
def menu_frep(user_id: int) -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()

    keyboard.row(
        rkb("🚑 Поддержка"), rkb("👤 Профиль"),
    )

    if user_id in get_admins():
        keyboard.row(
            rkb("👨‍💻 Админка"),
        )

    return keyboard.as_markup(resize_keyboard=True)