from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from create_bot import dp, bot
from aiogram.dispatcher.filters import Text
from data_base import sqlite_db
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards.all_kb import kb_client

############################################################# MENU #############################################################

async def start(message: types.Message):
	await message.answer('Привет это бот BlessStore', reply_markup=kb_client)
	
async def show_menu(message: types.Message):
	for ret in sqlite_db.cur.execute('SELECT * FROM crossovki').fetchall():
		await bot.send_photo(message.from_user.id, ret[0])
		await bot.send_photo(message.from_user.id, ret[1], f'Название: {ret[2]}\nРазмер: {ret[3]}\nАйди: {ret[4]}')
	
############################################################# SAERCH #############################################################


class FSMAdmin(StatesGroup):
	messsss = State()

async def search(message: types.Message):
	await FSMAdmin.messsss.set()
	await message.reply('Название для поиска')

async def search_write(message: types.Message, state: FSMContext):
	async with state.proxy() as data:
		data['messsss'] = message.text

	await state.finish()

	textttt = data['messsss']

	sqlite_db.cur.execute('SELECT img, img2, name, size, ids FROM crossovki WHERE name = ?', (textttt,))
	result = sqlite_db.cur.fetchmany(6)

	if result:
		for value in result:
			await bot.send_photo(message.from_user.id, value[0])
			await bot.send_photo(message.from_user.id, value[1], f'Название: {value[2]}\n Размер: {value[3]}\n Айди: {value[4]}')
	else:
		response = f'Нет информации по запросу в базе данных.'
		await message.answer(response)


############################################################# CANCLE #############################################################


async def cancel_handler1(message: types.Message, state: FSMContext):
	current_state = await state.get_state()
	if current_state is None:
		return
	await state.finish()
	await message.reply('OK')


############################################################# ALL FUCTION #############################################################

def register_handlers_client(dp: Dispatcher):
	dp.register_message_handler(start, commands=['start'])
	dp.register_message_handler(show_menu, commands=['all_crossovki'])
	
	dp.register_message_handler(search, commands='search', state=None)
	dp.register_message_handler(search_write, state=FSMAdmin.messsss)
	
	dp.register_message_handler(cancel_handler1, state="*", commands='отмена')
	dp.register_message_handler(cancel_handler1, Text(equals='отмена', ignore_case=True), state="*")
