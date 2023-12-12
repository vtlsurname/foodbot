from main import bot, dp 
from aiogram.types import Message
from keyboard.user_kb import user_main_menu
from base.bd_funcs import is_user_in_bd, add_user_in_bd
from inline_keyboard.main_board import get_main_menu
from base.bd_funcs import set_message_id, get_message_id


@dp.message_handler(text='/start')
async def start_func(message: Message):
    user_id=message.from_id
    menu = get_main_menu()
    msg_id = get_message_id(user_id)

    try:
        await bot.delete_message(chat_id=user_id, message_id=msg_id)
    except:
        pass

    if is_user_in_bd(user_id=user_id):
        msg = await message.answer(text=f'Привіт, <b>{message.from_user.full_name}</b>.', reply_markup=menu)
        set_message_id(user_id, message_id=msg["message_id"])
    else:
        add_user_in_bd(user_id=user_id)
        msg = await message.answer(text=f'Привіт, <b>{message.from_user.full_name}</b>.\nДодав тебе у БД!', reply_markup=menu)
        set_message_id(user_id, message_id=msg["message_id"])
