# - *- coding: utf- 8 - *-
from aiogram import Dispatcher, F

from bot.routers import main_errors, main_missed, main_start
from bot.routers.admin import admin_menu, admin_settings, admin_func
from bot.routers.user import user_menu
from bot.utils.misc.bot_filters import IsAdmin


# Регистрация всех роутеров
def register_all_routers(dp: Dispatcher):
    # Подключение фильтров
    main_errors.router.message.filter(F.chat.type == "private")
    main_start.router.message.filter(F.chat.type == "private")

    user_menu.router.message.filter(F.chat.type == "private")
    admin_menu.router.message.filter(F.chat.type == "private", IsAdmin())
    admin_settings.router.message.filter(F.chat.type == "private", IsAdmin())
    admin_func.router.message.filter(F.chat.type == "private", IsAdmin())

    main_missed.router.message.filter(F.chat.type == "private")

    # Подключение обязательных роутеров
    dp.include_router(main_errors.router)  # Роутер ошибки
    dp.include_router(main_start.router)  # Роутер основных команд

    # Подключение пользовательских роутеров (юзеров и админов)
    dp.include_router(user_menu.router)  # Юзер роутер
    dp.include_router(admin_menu.router)  # Админ роутер
    dp.include_router(admin_settings.router)  # Админ-настройки роутер
    dp.include_router(admin_func.router)  # Админ-функции роутер

    # Подключение обязательных роутеров
    dp.include_router(main_missed.router)  # Роутер пропущенных апдейтов