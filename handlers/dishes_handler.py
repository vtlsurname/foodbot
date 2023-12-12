from itertools import product
from main import bot, dp 
from aiogram.types import Message
from keyboard.user_kb import user_main_menu
from inline_keyboard.dishes_board import get_categories_menu, get_dishes_menu
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import CallbackQuery
from cfg import admin_id
from aiogram import types
from keyboard.order_kb import get_dish_info, get_order_board
from base.bd_funcs import set_message_id, get_message_id, update_basket
from base.bd_funcs import make_dish_preview_message, get_blacklist_users


@dp.callback_query_handler(text='Категорії')
async def print_dishes_categories(call: CallbackQuery):
    banned_users = get_blacklist_users()
    user_id = call.from_user.id
    msg_id = get_message_id(user_id)

    if user_id in banned_users:
        await bot.send_message(chat_id=user_id, text='Ви не можете користуватися цією функцією')
    else:
        try:
            await bot.delete_message(chat_id=user_id, message_id=msg_id)
        except Exception:
            pass
        
        categories_menu = get_categories_menu() # получаем клавиатуру Категорий
        
        msg = await bot.send_message(chat_id=user_id, text='Ось наші Меню', reply_markup=categories_menu) # делаем переменную для сохранения айди сообщения
        set_message_id(user_id=user_id, message_id=int(msg["message_id"])) # обновляем меседж айди


@dp.callback_query_handler(text_contains='food_categori')
async def dish_categoria_func(call: CallbackQuery):
    data = call.data
    user_id = call.from_user.id
    message_id = get_message_id(user_id=call.from_user.id)
    categori_name = data.replace('food_categori_', '')

    menu = get_dishes_menu(categoria=categori_name)
    
    await bot.edit_message_text(message_id=message_id, chat_id=call.from_user.id, text=f'Виберіть страву', reply_markup=menu)


@dp.callback_query_handler(text_contains='food')
async def food_func(call: CallbackQuery):
    data=call.data
    food_name = data.replace('food_', '')
    message_id = get_message_id(user_id=call.from_user.id)

    menu = get_order_board(name=food_name)
    
    message_text = make_dish_preview_message(food_name)

    user_id = call.from_user.id
    msg_id = get_message_id(user_id)

    try:
        await bot.delete_message(chat_id=user_id, message_id=msg_id)

        try:
            with open(f'images/{food_name}.png', 'rb') as f:
                msg = await bot.send_photo(chat_id = user_id, photo=f, caption=message_text, reply_markup=menu)
                set_message_id(user_id=user_id, message_id=int(msg["message_id"]))
        except:
            msg = await bot.send_message(chat_id=user_id, text=message_text, reply_markup=menu)
            set_message_id(user_id=user_id, message_id=int(msg["message_id"]))

    except:
        pass

@dp.callback_query_handler(text_contains='add_to_basket_')
async def add_to_basket_dish(callback_query: types.CallbackQuery):
    menu = get_categories_menu()
    user_id = callback_query.from_user.id
    msg_id = get_message_id(user_id=callback_query.from_user.id)
    data = callback_query.data
    product_name = data.replace('add_to_basket_', '')
    
    update_basket(user_id=callback_query.from_user.id, product_name=product_name)

    try:
        await bot.delete_message(chat_id=user_id, message_id=msg_id)

        try:
            msg = await bot.send_message(chat_id=user_id, text='Додав товар у кошик✔', reply_markup=menu)
            set_message_id(user_id=user_id, message_id=int(msg["message_id"]))
        except Exception as ex:
            print(ex)
    except Exception as ex:
            print(ex)

@dp.callback_query_handler(text='cencel_to_basket')
async def cencel_to_basket_dish(call: CallbackQuery):
    menu = get_categories_menu()
    user_id = call.from_user.id
    msg_id = get_message_id(user_id=call.from_user.id)

    
    try:
        await bot.delete_message(chat_id=user_id, message_id=msg_id)

        msg = await bot.send_message(chat_id=user_id, text='Ось наші Меню', reply_markup=menu)
        set_message_id(user_id=user_id, message_id=int(msg["message_id"]))

    except Exception as ex:
        print(ex)