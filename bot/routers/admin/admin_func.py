# - *- coding: utf- 8 - *-
from aiogram import Router, Bot, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
import asyncio

from bot.data.config import db
from bot.utils.misc.bot_models import FSM, ARS
from bot.keyboards.inline_admin import admin_func_inl
from bot.keyboards.inline_helper import cancel_inl
from aiogram.filters import StateFilter
from bot.utils.const_functions import ded, smart_message, get_unix

router = Router(name=__name__)

# Открытие админ функций 
@router.message(F.text == "🔆 Функции")
async def open_func_menu(message: Message, bot: Bot, state: FSM, arSession: ARS):
    await state.clear()
    
    await message.answer(
        "Функции администратора", 
        reply_markup=admin_func_inl()
    )
    
@router.callback_query(F.data == "admin_func")
async def open_func_menu_call(message: Message, bot: Bot, state: FSM, arSession: ARS):
    await state.clear()
    
    await message.answer(
        "Функции администратора", 
        reply_markup=admin_func_inl()
    )
    
@router.callback_query(F.data == "newsletter")
async def newsletter(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS):
    await state.clear()
    await call.message.edit_text(
        ded(
            """Введите сообщение для рассылки 
            
            <b>(можно отправлять фото/видео/gif и использовать разметку Telegram)</b>"""
            ), 
        reply_markup=cancel_inl('admin_func')
    )
    await state.set_state("newsletter_msg")
    
@router.message((F.text) | (F.photo) | (F.animation) | (F.video), StateFilter("newsletter_msg"))
async def get_newsletter_msg(message: Message, bot: Bot, state: FSM, arSession: ARS):
    users = await db.all_users()
    yes_users, no_users  = 0, 0
    photo = None
    video = None
    gif = None
    
    get_time = get_unix()
    
    if message.photo:
        photo = message.photo[-1].file_id
        text = message.html_text
    elif message.video:
        video = message.video.file_id
        text = message.html_text
    elif message.animation:
        gif = message.animation.file_id
        text = message.html_text
    else:
        text = message.text
        
    for user in users:
        try:
            await smart_message(bot, user['user_id'], text, photo=photo, video=video, gif=gif)
            yes_users += 1
        except Exception as e:
            print(f"Error sending message to user {user['user_id']}: {e}")
            no_users += 1
            
        edit_message = message.answer("<b>📢 Рассылка началась...</b>")
            
    new_msg = ded(f"""
    <b>📢 Рассылка была завершена за <code>{get_unix() - get_time}сек</code></b>
    
    <b>👤 Всего пользователей: <code>{len(await db.all_users())}</code>
    ✅ Отправлено: <code>{yes_users}</code>
    ❌ Не отправлено: <code>{no_users}</code></b>
    """)

    await message.answer(new_msg)
    await state.clear()