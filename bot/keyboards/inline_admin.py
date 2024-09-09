# - *- coding: utf- 8 - *-
from typing import Union

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.utils.const_functions import ikb

# Меню редактирования настроек
def admin_settings_inl() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        ikb("🚑 Поддержка", data='open:support')
    ).row(
        ikb("📝 Информация", data='open:info')
    )

    return keyboard.as_markup()

def admin_settings_edit_inl(data) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        ikb("🖊️ Изменить", data=f'edit:{data}')
    ).row(
        ikb("🔙 Назад", data=f'settings')
    )
    return keyboard.as_markup()

