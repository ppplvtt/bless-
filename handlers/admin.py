from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from create_bot import dp, bot
from aiogram.dispatcher.filters import Text
from data_base import sqlite_db
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards.all_kb import kb_admin

ID3 = False
product_id = 0


############################################################# ADMIN #############################################################

async def autor_admin(message: types.Message):
	user = message.from_user
	admin_teg = user.username

	for ret4 in sqlite_db.cur.execute('SELECT admin_id FROM admins').fetchall():
		if ret4[0] == admin_teg:
			global ID3
			ID3 = True
			await message.answer('Вы успешно авторизовались как админ!', reply_markup=kb_admin)

		
		else:
			await message.answer('Вы не админ бота!')

class FSMAdmin1(StatesGroup):
	admin_id = State()

async def cm_start1(message: types.Message):
	# if ID3 == True:
		await FSMAdmin1.admin_id.set()
		await message.reply('Загрузи ид админа')

async def load_admin_id(message: types.Message, state: FSMContext):
	# if ID3 == True:
		async with state.proxy() as data:
			data['admin_id'] = message.text

		await message.reply("Вы успешно добавили админа!")
		await state.finish()

		admins = data['admin_id']
		sqlite_db.cur.execute('INSERT INTO admins (admin_id) VALUES (?)', (admins, ))
		sqlite_db.base.commit()

async def sql_read(message):
	for ret3 in sqlite_db.cur.execute('SELECT admin_id FROM admins').fetchall():
		await bot.send_message(message.from_user.id, f'Админ: {ret3[0]}')

############################################################# crossovki #############################################################

class FSMAdmin(StatesGroup):
	photo1 = State()
	photo2 = State()
	name = State()
	reservation = State()
	size = State()
	ids = State()
	
async def cm_start(message: types.Message):
	if ID3 == True:
		await FSMAdmin.photo1.set()
		await message.reply('Загрузи фото сайзтега')

async def load_photo(message: types.Message, state: FSMContext):
	if ID3 == True:
		async with state.proxy() as data:
			data['photo1'] = message.photo[0].file_id
		await FSMAdmin.next()
		await message.reply("Теперь загрузи фото бирки")

async def load_photo2(message: types.Message, state: FSMContext):
	if ID3 == True:
		async with state.proxy() as data:
			data['photo2'] = message.photo[0].file_id
		await FSMAdmin.next()
		await message.reply("Теперь введи название")

async def load_name(message: types.Message, state: FSMContext):
	if ID3 == True:
		async with state.proxy() as data:
			data['name'] = message.text
		await FSMAdmin.next()
		await message.reply("Теперь введи бронь")

async def load_reservation(message: types.Message, state: FSMContext):
	if ID3 == True:
		async with state.proxy() as data:
			data['reservation'] = message.text
		await FSMAdmin.next()
		await message.reply("Теперь введи размер")

async def load_size(message: types.Message, state: FSMContext):
	if ID3 == True:
		async with state.proxy() as data:
			data['size'] = message.text
		
		await message.reply("Вы успешно добавили новый продукт!")
		await state.finish()

		global product_id
		product_id += 1

		photo1 = data['photo1']
		photo2 = data['photo2']
		name = data['name']
		reservation = data['reservation']
		size = data['size']
		
		sqlite_db.cur.execute('INSERT INTO crossovki (img, img2, name, size, ids, reservation) VALUES (?, ?, ?, ?, ?, ?)', (photo1, photo2, name, size, product_id, reservation))
		sqlite_db.base.commit()


############################################################# DEL CROSSOVKI #############################################################


class FSMAdmin2(StatesGroup):
	message_delete = State()

async def delete(message: types.Message):
	if ID3 == True:
		await FSMAdmin2.message_delete.set()
		await message.reply('Айдишник для поиска')

async def delete_write(message: types.Message, state: FSMContext):
	if ID3 == True:
		async with state.proxy() as data:
			data['message_delete'] = message.text

		await state.finish()

		textttt = data['message_delete']

		sqlite_db.cur.execute('SELECT img, img2, name, size, ids FROM crossovki WHERE ids = ?', (textttt,))
		result = sqlite_db.cur.fetchmany(6)

		if result:
			for value in result:
				await bot.send_photo(message.from_user.id, value[0])
				await bot.send_photo(message.from_user.id, value[1], f'Название: {value[2]}\n Размер: {value[3]}\n Айди: {value[4]}')
				sqlite_db.cur.execute('DELETE FROM crossovki WHERE ids == ?', (textttt,)) 
				sqlite_db.base.commit()
				await message.answer(f'Продукт с айдишником {value[4]} удалён')
		else:
			response = f'Нет указанного айдишника в базе данных.'
			await message.answer(response)

	
############################################################# CANCEL #############################################################


async def cancel_handler(message: types.Message, state: FSMContext):
	if ID3 == True:
		current_state = await state.get_state()
		if current_state is None:
			return
		await state.finish()
		await message.reply('OK')


############################################################# ALL FUNC #############################################################

def register_handlers_admin(dp: Dispatcher):
	dp.register_message_handler(autor_admin, commands=['admin'])
	dp.register_message_handler(sql_read, commands='all_admin')
	dp.register_message_handler(cm_start1, commands='add_admin', State=None)
	dp.register_message_handler(load_admin_id, state=FSMAdmin1.admin_id)

	dp.register_message_handler(cm_start, commands='new_crossovki', state=None)
	dp.register_message_handler(load_photo, content_types=['photo'], state=FSMAdmin.photo1)
	dp.register_message_handler(load_photo2, content_types=['photo'], state=FSMAdmin.photo2)
	dp.register_message_handler(load_name, state=FSMAdmin.name)
	dp.register_message_handler(load_reservation, state=FSMAdmin.reservation)
	dp.register_message_handler(load_size, state=FSMAdmin.size)
	

	dp.register_message_handler(delete, commands='delete', state=None)
	dp.register_message_handler(delete_write, state=FSMAdmin2.message_delete)

	
	dp.register_message_handler(cancel_handler, state="*", commands='отмена')
	dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state="*")
