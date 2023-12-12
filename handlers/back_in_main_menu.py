from main import bot, dp 
from aiogram import types
from aiogram.types import CallbackQuery
from inline_keyboard.main_board import get_main_menu
from base.bd_funcs import get_message_id


@dp.callback_query_handler(text='Головне меню')
async def back_in_main_menu(call: CallbackQuery):
    menu = get_main_menu()
    message_id = get_message_id(user_id=call.from_user.id)

    await bot.edit_message_text(message_id=message_id, chat_id=call.from_user.id, text=f'Головне меню', reply_markup=menu)
