from aiogram import Bot, Dispatcher, executor
import asyncio
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from cfg import token


storage = MemoryStorage()
loop = asyncio.get_event_loop()
bot = Bot(token, parse_mode="HTML")
dp = Dispatcher(bot, loop, storage)


if __name__ == "__main__":
    from all_handlers import dp
    executor.start_polling(dp)
