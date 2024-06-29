from aiogram.utils import executor
from create_bot import dp
from data_base import sqlite_db
from handlers import client, admin

async def on_startup(_):	
	sqlite_db.sql_start()



admin.register_handlers_admin(dp)
client.register_handlers_client(dp)


	
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
