from aiogram import Bot
from aiogram.dispatcher import Dispatcher
import os
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()

API_TOKEN = '7073895277:AAGqp54Oz-8us8mLVLuvWTT9pg4S-aSm25w'
bot = Bot(token=API_TOKEN)

dp = Dispatcher(bot, storage=storage)
