# - *- coding: utf- 8 - *-

from aiogram.types import InlineKeyboardButton
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.utils.const_functions import ikb

def cancel_inl(data) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        ikb("⛔ Отмена", data=data)
    )
    return keyboard.as_markup()

