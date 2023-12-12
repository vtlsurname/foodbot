from main import bot, dp 
from aiogram.types import Message, CallbackQuery
from cfg import admin_id
from base.bd_funcs import profile_message, get_message_id, set_message_id,update_user_phone
from inline_keyboard.profile_board import get_profile_menu
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from inline_keyboard.main_board import get_main_menu, back_in_menu


@dp.callback_query_handler(text='Профіль')
async def show_profile(call:CallbackQuery):
    user_id = call.from_user.id
    message_text = profile_message(user_id)
    msg_id = get_message_id(user_id)
    menu = get_profile_menu()

    await bot.edit_message_text(chat_id=user_id, message_id=msg_id, text=message_text, reply_markup=menu)


class change_phone_class(StatesGroup):
    new_phone = State()

@dp.callback_query_handler(text='Змінити номер телефону')
async def start_change_phone(call: CallbackQuery):
    user_id = call.from_user.id
    msg_id = get_message_id(user_id)
    
    try:
        await bot.delete_message(chat_id=user_id, message_id=msg_id)
    except:
        pass
        
    
    await bot.send_message(chat_id=user_id, text='Напишіть новий номр телефону\nДля того щоб відмінити дію напишіть: cencel')
    # set_message_id(user_id ,message_id=msg['message_id'])

    await change_phone_class.new_phone.set()

@dp.message_handler(state=change_phone_class.new_phone)
async def end_change_phone(message:Message, state: FSMContext):
    answer = message.text
    user_id = message.from_id
    msg_id = get_message_id(user_id)
    
    if answer == 'cencel':
        menu=get_main_menu()
        msg = await bot.send_message(chat_id=user_id, text='Дія зупинена', reply_markup=menu)
        set_message_id(user_id=user_id, message_id=msg["message_id"])

        await state.finish()
    else:
        try:
            menu = get_profile_menu()
            update_user_phone(user_id=user_id, user_phone=answer)
            
            message_text = profile_message(user_id)
            msg = await bot.send_message(chat_id=user_id, text=message_text, reply_markup=menu)
            set_message_id(user_id=user_id, message_id=msg["message_id"])
            
            await state.finish()

        except:
            menu = back_in_menu()
            msg = await bot.send_message(chat_id=user_id, text='Не вдалося змінити номер телефону', reply_markup=menu)
            set_message_id(user_id=user_id, message_id=msg["message_id"])

            await state.finish