from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import aioredis

from config import token

storage = MemoryStorage()

bot = Bot(token=token, parse_mode='HTML')
dp = Dispatcher(bot, storage=storage)

redis = aioredis.from_url("redis://localhost:6379")  # Локальный Redis