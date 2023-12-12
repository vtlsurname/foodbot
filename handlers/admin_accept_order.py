from main import bot, dp
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import sqlite3, json
from aiogram.types import CallbackQuery
from base.bd_funcs import get_order, delete_order, get_admin_ids_from_database, get_phone_by_user_id, get_chef_ids_from_database
from aiogram.types import Message
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext


# Функция для получения списка заказов из базы данных
def get_orders():
    conn = sqlite3.connect("base.db")
    cur = conn.cursor()

    cur.execute("SELECT DISTINCT user_id FROM orders")
    orders = cur.fetchall()

    conn.close()
    return orders


@dp.message_handler(text='Замовлення')
async def orders_handler(message:Message):
    admin_ids = get_admin_ids_from_database()
    
    if message.from_id in admin_ids:
        # Получаем список заказов
        orders = get_orders()

        # Формируем инлайн-кнопки с заказами
        keyboard = InlineKeyboardMarkup(row_width=1)
        for order in orders:
            user_id = order[0]
            button_text = f"Замовлення {user_id}"
            button = InlineKeyboardButton(text=button_text, callback_data=f"order:{user_id}")
            keyboard.add(button)

        # Отправляем сообщение с инлайн-кнопками
        await message.answer("Замовлення в очікуванні", reply_markup=keyboard)
    else:
        await message.answer(text='You are not an admin')

class ConfirmOrder(StatesGroup):
    getDescription = State()


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('order:'))
async def process_order_callback(callback_query: CallbackQuery):
    order_id = callback_query.data.split(':')[1]
    user_phone = get_phone_by_user_id(order_id)

    conn = sqlite3.connect("base.db")
    cur = conn.cursor()
    cur.execute("SELECT dish_order FROM orders WHERE user_id=?", (order_id,))
    dishes = cur.fetchone()
    
    if dishes:
        message_text = f"Замовлення {order_id}\nСтрави:\n{dishes[0]}\nНомер телефону: {user_phone}"
        keyboard = InlineKeyboardMarkup()
        keyboard.add(
            InlineKeyboardButton(text="Підтвердити", callback_data=f"confirm:{order_id}"),
            InlineKeyboardButton(text="Відмінити", callback_data=f"cancel:{order_id}")
        )
        await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text=message_text, reply_markup=keyboard)
    else:
        await bot.answer_callback_query(callback_query.id, text="Це замовлення не знайдено", show_alert=True)
        return
    conn.close()

    @dp.callback_query_handler(lambda c: c.data and c.data == f"confirm:{order_id}")
    async def confirm_order_callback(callback_query: CallbackQuery, state:FSMContext):
        order_id = callback_query.data.split(':')[1]
        
        # Проверяем, есть ли уже заказ с таким user_id в базе
        with sqlite3.connect("base.db") as conn:
            # Получаем заказ по ID
            order = get_order(order_id)
            user_id = order[0]
            dishes = order[1]
            
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM chef_orders WHERE user_id = ?", (user_id,))
            existing_order = cursor.fetchone()
            if existing_order:
                # Если заказ уже есть, выводим сообщение и выходим из функции
                await bot.answer_callback_query(callback_query.id, text=f"Замовлення від користувача {user_id} вже існує в базі.")
                return

            # Запрашиваем у пользователя описание к заказу
            await bot.answer_callback_query(callback_query.id)
            await bot.send_message(chat_id=callback_query.message.chat.id, text='Введіть опис замовлення:')
            
            # Устанавливаем состояние для получения описания к заказу
            await ConfirmOrder.getDescription.set()

            # Записываем ID заказа в контекст, чтобы использовать его в следующих хэндлерах
            await state.update_data(order_id=order_id)

        
@dp.message_handler(state=ConfirmOrder.getDescription)
async def get_description(callback_query: CallbackQuery, state: FSMContext):
    # Получаем ID заказа из контекста
    async with state.proxy() as data:
        order_id = data["order_id"]

    # Записываем описание в базу данных chef_orders
    with sqlite3.connect("base.db") as conn:
        order = get_order(order_id)
        user_id = order[0]
        dishes = order[1]
        
        cursor = conn.cursor()
        cursor.execute("INSERT INTO chef_orders (user_id, dish_order, admin_not) VALUES (?, ?, ?)", (user_id, dishes, callback_query.text))
        conn.commit()

    # Удаляем заказ из таблицы orders
    delete_order(order_id)

    # Формируем список заказов
    orders = get_orders()

    # Формируем инлайн-кнопки с заказами
    keyboard = InlineKeyboardMarkup(row_width=1)
    for order in orders:
        user_id = order[0]
        button_text = f"Замовлення {user_id}"
        button = InlineKeyboardButton(text=button_text, callback_data=f"order:{user_id}")
        keyboard.add(button)

    try:
        await bot.send_message(chat_id=user_id, text='Ваше замовлення було підтверджене.')
    except:
        pass

    chef_ids = get_chef_ids_from_database()
    for chef_id in chef_ids:
        try:
            await bot.send_message(chat_id=chef_id, text=f'У вас нове замовлення <b>{order_id}</b>! Для перегляду всіх поточних замовлень напишіть /chef')
        except:
            pass

    # Отправляем сообщение с инлайн-кнопками
    await bot.send_message(chat_id=callback_query.chat.id, text=f"Замовлення {order_id} підтверджено", reply_markup=keyboard)
    #await bot.answer_callback_query(callback_query.id, text=f"Замовлення {order_id} було підтверджено")
    await state.finish()


@dp.callback_query_handler(lambda c: c.data and c.data.startswith("cancel:"))
async def cancel_order_callback(callback_query: CallbackQuery):
    order_id = callback_query.data.split(':')[1]
    conn = sqlite3.connect("base.db")
    cur = conn.cursor()
    cur.execute("SELECT dish_order FROM orders WHERE user_id=?", (order_id,))
    dishes = cur.fetchone()
    if dishes:
        dish_list = [dish.strip() for dish in dishes[0].split(",")]
        order_data = {"user_id": order_id, "dish_list": dish_list}
        file_path = f"basket_base/{order_id}.json"
        with open(file_path, "w") as f:
            json.dump(order_data, f)

        # Удаление заказа из базы данных
        cur.execute("DELETE FROM orders WHERE user_id=?", (order_id,))
        conn.commit()

        # print(f"Список страв користувача {order_id}: {dishes[0]}")
    else:
        pass
        # print(f"Список страв користувача {order_id} не знайдений")
    conn.close()

    # Получаем список заказов
    orders = get_orders()

    # Формируем инлайн-кнопки с заказами
    keyboard = InlineKeyboardMarkup(row_width=1)
    for order in orders:
        user_id = order[0]
        button_text = f"Заказ {user_id}"
        button = InlineKeyboardButton(text=button_text, callback_data=f"order:{user_id}")
        keyboard.add(button)

    try:
        await bot.send_message(chat_id=order_id, text='Ваше замовлення було скасоване.')
    except:
        pass

    # Отправляем сообщение с инлайн-кнопками
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text=f"Замовлення {order_id} було скасовано", reply_markup=keyboard)
    await bot.answer_callback_query(callback_query.id, text=f"Замовлення {order_id} було скасовано")
