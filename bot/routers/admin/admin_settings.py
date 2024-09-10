# - *- coding: utf- 8 - *-
from aiogram import Router, Bot, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from bot.data.config import db
from bot.utils.misc.bot_models import FSM, ARS
from bot.keyboards.inline_admin import admin_settings_inl, admin_settings_edit_inl
from bot.keyboards.inline_helper import cancel_inl
from aiogram.filters import StateFilter

router = Router(name=__name__)

# Открытие мнастроек из меню даминистратора
@router.message(F.text == "⚙ Настройки")
async def admin_settings_menu_message(message: Message, bot: Bot, state: FSM, arSession: ARS):
    await state.clear()
    await message.answer("⚙ Меню настроек ", reply_markup=await admin_settings_inl())


@router.callback_query(F.data == "settings")
async def admin_settings_menu_call(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS):
    await state.clear()
    await call.message.edit_text(
        "⚙ Меню настроек ", 
        reply_markup=await admin_settings_inl()
    )
    
#Открытие редактирования
@router.callback_query(F.data.startswith("open:"))
async def admin_open_settings(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS):
    await state.clear()
    data = call.data.split(":")[1]
    settings = await db.get_settings(id=1)
    if data == 'support':
        if settings['support'] == '':
            support_link = "<code>не установлено</code>"
        else:
            support_link = f"<a href='{settings['support']}'>саппорт</a>"
        await call.message.edit_text(f"Ссылка на подддержку: {support_link}", 
                                     reply_markup=admin_settings_edit_inl(data=data))
    elif data == 'info':
        if settings['info'] == '':
            info = "<code>Информация не установлена</code>"
        else:
            info = settings['info']
        await call.message.edit_text(info, 
                                     reply_markup=admin_settings_edit_inl(data=data))

# Редактирование настроек 
@router.callback_query(F.data.startswith("edit:"))
async def admin_edit_settings(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS):
    await state.clear()
    await call.message.delete()
    data = call.data.split(":")[1]
    if data == 'support':
        text = "Укажите ссылку на поддержку в формате <code>https://t.me/юзернейм</code>"
    elif data == 'info':
        text = "Введите информацию, можно использовать разметку Telegram"
    await call.message.answer(text=text, reply_markup=cancel_inl(data=f"open:{data}"))
    await state.update_data(settings_edit_param=data)
    await state.set_state("settings_edit")

@router.message(F.text, StateFilter("settings_edit"))
async def admin_save_settings(message: Message, bot: Bot, state: FSM, arSession: ARS):
    param = (await state.get_data())['settings_edit_param']
    await state.clear()
    if param == "support":
        if 'https://t.me/' in message.text:
            await db.update_settings(support=message.text)
            await message.answer("Ссылка на Поддержку успешно обновлена")
        else: 
            await message.answer("<b>Ошибка!</b> Ссыка должна начинаться с <code>https://t.me/</code>")
    if param == 'info':
        parse_msg = message.html_text
        print(parse_msg)
        await db.update_settings(info=parse_msg)
        await message.answer("Информация успешно обновлена")
    await state.finish()

# Включение / отключение тех. работ
@router.callback_query(F.data.startswith("edit_work:"))
async def admin_edit_settings(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS):
    await state.clear()
    data = call.data.split(":")[1]
    if data == 'turnOn':
        await db.update_settings(is_work="False")
        await call.answer("Режим тех. работ: Включен")
    else: 
        await db.update_settings(is_work="True")
        await call.answer("Режим тех. работ: Выключен")
    await call.message.delete()
    await call.message.answer("⚙ Меню настроек ", reply_markup=await admin_settings_inl())