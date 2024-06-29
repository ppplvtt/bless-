import sqlite3 as sq
from create_bot import bot

def sql_start():
	global base, cur
	base = sq.connect('shop.db')
	cur = base.cursor()
	if base:
		print('Data base connected OK!')
	base.execute('CREATE TABLE IF NOT EXISTS crossovki(img TEXT, img2 TEXT, name TEXT, size TEXT, ids TEXT, reservation TEXT)')
	base.execute('CREATE TABLE IF NOT EXISTS admins(admin_id TEXT)')
	base.commit()


