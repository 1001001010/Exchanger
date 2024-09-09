# - *- coding: utf- 8 - *-
import configparser
import asyncio

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from bot.data.db import DB

# Создание экземпляра бд 
async def main_db():
    db = await DB()

    return db

loop = asyncio.get_event_loop()
task = loop.create_task(main_db())
db = loop.run_until_complete(task)

# Токен бота
BOT_TOKEN = configparser.ConfigParser()
BOT_TOKEN.read("settings.ini")
BOT_TOKEN = BOT_TOKEN['settings']['bot_token'].strip().replace(' ', '')

# Пути к файлам
PATH_DATABASE = "bot/data/database.db"  # Путь к БД
PATH_LOGS = "bot/data/logs.log"  # Путь к Логам

# Образы и конфиги
BOT_STATUS_NOTIFICATION = False  # Оповещение админам о запуске бота (True или False)
BOT_TIMEZONE = "Europe/Moscow"  # Временная зона бота
BOT_SCHEDULER = AsyncIOScheduler(timezone=BOT_TIMEZONE)  # Образ шедулера


# Получение администраторов бота
def get_admins() -> list[int]:
    read_admins = configparser.ConfigParser()
    read_admins.read('settings.ini')

    admins = read_admins['settings']['admin_id'].strip().replace(" ", "")

    if "," in admins:
        admins = admins.split(",")
    else:
        if len(admins) >= 1:
            admins = [admins]
        else:
            admins = []

    while "" in admins: admins.remove("")
    while " " in admins: admins.remove(" ")
    while "," in admins: admins.remove(",")
    while "\r" in admins: admins.remove("\r")
    while "\n" in admins: admins.remove("\n")

    return list(map(int, admins))