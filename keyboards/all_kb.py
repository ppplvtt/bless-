from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

btn_menu = KeyboardButton('/all_crossovki')
btn_search = KeyboardButton('/search')
kb_client = ReplyKeyboardMarkup()
kb_client.add(btn_menu, btn_search)


btn_admin1 = KeyboardButton('/all_crossovki')

btn_admin2 = KeyboardButton('/new_crossovki')

btn_admin3 = KeyboardButton('/delete')

btn_admin4 = KeyboardButton('/add_admin')
btn_admin5 = KeyboardButton('/all_admin')

btn_admin6 = KeyboardButton('/search')

kb_admin = ReplyKeyboardMarkup(resize_keyboard=True)
kb_admin.add(btn_admin1, btn_admin2, btn_admin3)
kb_admin.add(btn_admin4, btn_admin5, btn_admin6)
