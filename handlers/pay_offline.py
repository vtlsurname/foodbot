from main import bot, dp 
from aiogram.types import CallbackQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from base.bd_funcs import save_order_to_db
from inline_keyboard.main_board import get_main_menu
from base.bd_funcs import get_admin_ids_from_database
import sqlite3


@dp.callback_query_handler(lambda c: c.data == 'pay_offline')
async def pay_offline_handler(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()

    # получаем информацию о пользователе из базы данных
    cursor.execute(f"SELECT phone FROM users_info_bd WHERE user_id='{user_id}'")
    user_info = cursor.fetchone()

    if user_info is None or user_info[0] is None:
        message_text = "Для оплати потрібно додати номер телефону до вашого профілю. Натисніть /start, натисніть на кнопку профіль і змініть номер телефону."
        await bot.send_message(chat_id=user_id, text=message_text)
        return

    message_text = "Ви підтверджуєте це замовлення?"
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton("Так", callback_data="confirm_order"),
        InlineKeyboardButton("Ні", callback_data="cancel_order"),
    )
    await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                message_id=callback_query.message.message_id,
                                text=message_text,
                                reply_markup=keyboard)
    conn.close()

    
@dp.callback_query_handler(lambda c: c.data == 'confirm_order')
async def confirm_order_handler(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id 
    answer = save_order_to_db(user_id)
    admin_ids = get_admin_ids_from_database()
    
    for admin_id in admin_ids:
        try:
            await bot.send_message(chat_id=admin_id, text=f'У вас нове замовлення, <b>{user_id}</b>!')
        except:
            pass

    # получаем chat_id и message_id, чтобы изменить старое сообщение
    chat_id = callback_query.message.chat.id
    message_id = callback_query.message.message_id
    keyboard = get_main_menu()
    
    await bot.edit_message_text(chat_id=chat_id,
                                message_id=message_id,
                                text=answer,
                                reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data == 'cancel_order')
async def cancel_order_handler(callback_query: CallbackQuery):
    keyboard = get_main_menu()
    await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                message_id=callback_query.message.message_id,
                                text="Замовлення було скасовано",
                                reply_markup=keyboard)
    