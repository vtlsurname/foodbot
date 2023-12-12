from main import bot, dp 
from aiogram.types import Message
from base.bd_funcs import bot_statistic, get_admin_ids_from_database
from cfg import admin_id


@dp.message_handler(text='Статистика')
async def statistic(message:Message):
    user_id = message.from_id
    admin_ids = get_admin_ids_from_database()
    stat = bot_statistic()
    if user_id in admin_ids:
        await message.answer(text=f'Користувачів: {stat}')
    else:
        await message.answer(text='Ви не адмін!')
