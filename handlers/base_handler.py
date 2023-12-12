from main import bot, dp 
from aiogram.types import Message
from keyboard.admin_kb import base_menu
from base.bd_funcs import get_admin_ids_from_database


@dp.message_handler(text='БД')
async def open_base_menu(message:Message):
    user_id = message.from_id
    admin_ids = get_admin_ids_from_database()
    if user_id in admin_ids:
        await message.answer(text='Ви перейшли у меню для роботи з БД.', reply_markup=base_menu)
    else:
        await message.answer(text='Ви не адмін!')


@dp.message_handler(text='Завантажити БД')
async def download_base(message:Message):
    user_id = message.from_id
    admin_ids = get_admin_ids_from_database()
    if user_id in admin_ids:
        with open("base.db", 'rb') as f:
            await bot.send_document(chat_id=user_id, document=f)
    else:
        await message.answer(text='Ви не адмін!')
