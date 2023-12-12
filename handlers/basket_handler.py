from main import bot, dp 
from aiogram.types import Message
from base.bd_funcs import make_basket_message, del_dish_from_bskt, get_message_id, set_message_id, get_blacklist_users
from inline_keyboard.basket_board import get_basket_board
from inline_keyboard.main_board import back_in_menu
from aiogram.types import CallbackQuery
from inline_keyboard.basket_board import remove_from_basket


@dp.callback_query_handler(text='Кошик')
async def basket_func(call: CallbackQuery):
    user_id = call.from_user.id
    message_text = make_basket_message(user_id=user_id)
    msg_id = get_message_id(user_id=user_id)
    banned_users = get_blacklist_users()
    
    if user_id in banned_users:
        await bot.send_message(chat_id=user_id, text='Ви не можете користуватися цією функцією')
    else:
        if message_text != 'Ваш кошик пустий.':
            menu = get_basket_board()

            try:
                await bot.delete_message(chat_id=user_id, message_id=msg_id)
            except Exception:
                pass

            msg = await bot.send_message(chat_id=user_id, text=message_text, reply_markup=menu)
            set_message_id(user_id=user_id, message_id=msg["message_id"])

        else:
            menu = back_in_menu()
            await bot.edit_message_text(message_id=msg_id, chat_id=call.from_user.id, text=message_text, reply_markup=menu)
        

@dp.callback_query_handler(text='remove_from_basket')
async def remove_from_basket_func(call: CallbackQuery):
    menu = remove_from_basket(user_id=call.from_user.id)
    msg_id=get_message_id(user_id=call.from_user.id)

    await bot.edit_message_text(message_id=msg_id, chat_id=call.from_user.id, text='Що ви хочете видалити з вашого кошику?', reply_markup=menu)


@dp.callback_query_handler(text_contains='remove_basket_')
async def remove_from_basket_func(call: CallbackQuery):
    data = call.data
    user_id = call.from_user.id
    food_name = data.replace('remove_basket_', '')
    msg_id=get_message_id(user_id=call.from_user.id)

    del_dish_from_bskt(user_id, product_name=food_name)
    message_text = make_basket_message(user_id=user_id)
    
    if message_text != 'Ваш кошик пустий.':
        menu = get_basket_board()
        await bot.edit_message_text(message_id=msg_id, chat_id=call.from_user.id, text=message_text, reply_markup=menu)
    else:
        menu = back_in_menu()
        await bot.edit_message_text(message_id=msg_id, chat_id=call.from_user.id, text=message_text, reply_markup=menu)
