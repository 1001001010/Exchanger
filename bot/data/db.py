import aiosqlite
from async_class import AsyncClass
import time

PATH_DATABASE = "bot/data/database.db"  # Путь к БД

# Получение текущего unix времени (True - время в наносекундах, False - время в секундах)
def get_unix(full: bool = False) -> int:
    if full:
        return time.time_ns()
    else:
        return int(time.time())

#Преобразование результата в словарь
def dict_factory(cursor, row):
    save_dict = {}

    for idx, col in enumerate(cursor.description):
        save_dict[col[0]] = row[idx]

    return save_dict

# Форматирование запроса без аргументов
def query(sql, parameters: dict):
    if "XXX" not in sql: sql += " XXX "
    values = ", ".join([
        f"{item} = ?" for item in parameters
    ])
    sql = sql.replace("XXX", values)

    return sql, list(parameters.values())


# Форматирование запроса с аргументами
def query_args(sql, parameters: dict):
    sql = f"{sql} WHERE "

    sql += " AND ".join([
        f"{item} = ?" for item in parameters
    ])

    return sql, list(parameters.values())

#Проверка и создание бд
class DB(AsyncClass):
    async def __ainit__(self):
        self.con = await aiosqlite.connect(PATH_DATABASE)
        self.con.row_factory = dict_factory

    # Получение пользователя из БД
    async def get_user(self, **kwargs):
        queryy = "SELECT * FROM users"
        queryy, params = query_args(queryy, kwargs)
        row = await self.con.execute(queryy, params)
        return await row.fetchone()

    # Регистрация пользователя в БД
    async def register_user(self, user_id, user_name, first_name):
        await self.con.execute("INSERT INTO users("
                                "user_id, user_name, first_name, unix)"
                                "VALUES (?,?,?,?)",
                                [user_id, user_name, first_name, get_unix(full=False)])
        await self.con.commit()
        
    # Редактирование пользователя
    async def update_user(self, id, **kwargs):
        queryy = f"UPDATE users SET"
        queryy, params = query(queryy, kwargs)
        params.append(id)
        await self.con.execute(queryy + "WHERE user_id = ?", params)
        await self.con.commit()

    # Получение настроек
    async def get_settings(self, **kwargs):
        queryy = "SELECT * FROM settings"
        queryy, params = query_args(queryy, kwargs)
        row = await self.con.execute(queryy, params)
        return await row.fetchone()
    
    # Обновление настроек
    async def update_settings(self, **kwargs):
        queryy = "UPDATE settings SET"
        queryy, parameters = query(queryy, kwargs)
        await self.con.execute(queryy, parameters)
        await self.con.commit()
    
#Проверка на существование бд и ее создание
    async def create_db(self):
        users_info = await self.con.execute("PRAGMA table_info(users)")
        if len(await users_info.fetchall()) == 5:
            print("database was found (Users | 1/10)")
        else:
            await self.con.execute("CREATE TABLE users ("
                                   "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                                   "user_id INTEGER,"
                                   "user_name TEXT,"
                                   "first_name TEXT,"
                                   "unix INTEGER)")
            print("database was not found (Users | 1/10), creating...")
            await self.con.commit()
            
        settings_info = await self.con.execute("PRAGMA table_info(settings)")
        if len(await settings_info.fetchall()) == 4:
            print("database was found (Settings | 2/10)")
        else:
            await self.con.execute("CREATE TABLE settings ("
                                   "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                                   "is_work TEXT,"
                                   "support TEXT,"
                                   "info TEXT)")
            print("database was not found (Settings | 2/10), creating...")
            await self.con.execute("INSERT INTO settings("
                                            "is_work, support, info) "
                                            "VALUES (?, ?, ?)", ['True', '', ''])
            await self.con.commit()