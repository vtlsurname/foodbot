from main import bot, dp 
from aiogram.types import Message, CallbackQuery
from base.bd_funcs import get_chef_ids_from_database, get_chef_orders_from_database, get_ukr_time, save_order_to_history, get_chef_name, get_user_orders, delete_user_order
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from base.bd_funcs import get_admin_note, increase_user_purchases


@dp.message_handler(text='/chef')
async def get_chef_orders(message: Message):
    chef_ids = get_chef_ids_from_database()
    user_id = message.from_id
    
    if user_id not in chef_ids:
        await message.answer(text='Ви не кухар!')
        return
    
    orders = get_chef_orders_from_database()
    if not orders:
        await message.answer(text='Замовлень немає')
        return
    
    keyboard = InlineKeyboardMarkup(row_width=1)
    for order in orders:
        user_id, dish_order = order
        button_text = f"Замовлення {user_id}"
        button = InlineKeyboardButton(text=button_text, callback_data=f"chef_order:{user_id}")
        keyboard.add(button)
    
    await message.answer(text='Список замовлень:', reply_markup=keyboard)


    @dp.callback_query_handler(lambda c: c.data and c.data.startswith("chef_order:"))
    async def show_order_callback(callback_query: CallbackQuery):
        user_id = callback_query.data.split(':')[1]
        orders = get_chef_orders_from_database()
        
        if not orders:
            await bot.answer_callback_query(callback_query.id, text=f"Немає замовлень від користувача {user_id}")
            return
        
        order_id = orders[0][0]
        dishes = orders[0][1]
        admin_note = get_admin_note(order_id)
        
        #dish_list = ', '.join(dishes) # объединяем список блюд в одну строку через запятую
        
        keyboard = InlineKeyboardMarkup()
        confirm_button = InlineKeyboardButton(text="Підтвердити", callback_data=f"chef_confirm:{order_id}")
        dishes_button = InlineKeyboardButton(text="Список страв", callback_data=f"chef_dishes:{order_id}")
        keyboard.add(confirm_button, dishes_button)
        
        text = f"Замовлення: {user_id}\nСтрави: {dishes}\nНотатка від адміна: {admin_note}"
        await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text=text, reply_markup=keyboard)
        await bot.answer_callback_query(callback_query.id) 


@dp.callback_query_handler(lambda c: c.data and c.data.startswith("chef_dishes:"))
async def show_dishes_callback(callback_query: CallbackQuery):
    orders = get_chef_orders_from_database()
    
    if not orders:
        await bot.answer_callback_query(callback_query.id, text="Немає замовлень")
        return
    
    keyboard = InlineKeyboardMarkup(row_width=1)
    for order in orders:
        user_id, dish_order = order
        button_text = f"Замовлення {user_id}"
        button = InlineKeyboardButton(text=button_text, callback_data=f"chef_order:{user_id}")
        keyboard.add(button)
        
    text = "Список замовлень:"
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text=text, reply_markup=keyboard)
    await bot.answer_callback_query(callback_query.id)


@dp.callback_query_handler(lambda c: c.data and c.data.startswith("chef_confirm:"))
async def confirm_order_callback(callback_query: CallbackQuery):
    order_id = callback_query.data.split(':')[1]
    keyboard = InlineKeyboardMarkup()
    yes_button = InlineKeyboardButton(text="Так", callback_data=f"confirm_yes:{order_id}")
    no_button = InlineKeyboardButton(text="Ні", callback_data=f"confirm_no:{order_id}")
    keyboard.add(yes_button, no_button)
    text = "Ви точно виконали замовлення?"
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text=text, reply_markup=keyboard)
    await bot.answer_callback_query(callback_query.id)


@dp.callback_query_handler(lambda c: c.data and c.data.startswith("confirm_yes:"))
async def confirm_yes_callback(callback_query: CallbackQuery):
    chat_id = callback_query.message.chat.id
    order_id = callback_query.data.split(':')[1]
    now_time = get_ukr_time()
    chef_name = get_chef_name(chat_id=chat_id)
    user_dishes = get_user_orders(order_id)

    save_order_to_history(chef_id=chat_id, chef_name=chef_name, dish_order=user_dishes, time=now_time)
    delete_user_order(order_id)

    #confirm_order_in_database(order_id) # функция для обновления статуса заказа в базе данных
    text = "Дякуємо, замовлення підтверджено!"

    orders = get_chef_orders_from_database()

    try:
        await bot.send_message(chat_id=order_id, text='Ваше замовлення було виконано! ')
        increase_user_purchases(order_id)
    except:
        pass

    await bot.edit_message_text(chat_id=chat_id, message_id=callback_query.message.message_id, text=text)
    await bot.answer_callback_query(callback_query.id)

@dp.callback_query_handler(lambda c: c.data and c.data.startswith("confirm_no:"))
async def confirm_no_callback(callback_query: CallbackQuery):
    orders = get_chef_orders_from_database()
    if not orders:
        await bot.send_message(chat_id=callback_query.from_user.id, text='Замовлень немає')
        return
    
    keyboard = InlineKeyboardMarkup(row_width=1)
    for order in orders:
        user_id, dish_order = order
        button_text = f"Замовлення {user_id}"
        button = InlineKeyboardButton(text=button_text, callback_data=f"chef_order:{user_id}")
        keyboard.add(button)


    await bot.answer_callback_query(callback_query.id, text="Відмінено")
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text="Наступного разу подумайте перед дією.\nСписок замовлень:", reply_markup=keyboard)
