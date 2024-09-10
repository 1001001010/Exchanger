# - *- coding: utf- 8 - *-
from typing import Union

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.data.config import db
from bot.utils.const_functions import ikb

# Меню редактирования настроек
async def admin_settings_inl() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    info = await db.get_settings(id=1)
    keyboard.row(
        ikb("🚑 Поддержка", data='open:support'), ikb("📝 Информация", data='open:info')
    ).row(
        ikb(f"👷 {'Включить' if info['is_work'] == 'True' else 'Выключить'} Тех работы ", data=f"edit_work:{'turnOn' if info['is_work'] == 'True' else 'turnOff'}")
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

def admin_func_inl() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        ikb("📭 Рассылка", data=f'newsletter')  
    )
    return keyboard.as_markup()

