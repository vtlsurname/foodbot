from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import sqlite3, json


def get_basket_board():
    inline_menu = InlineKeyboardMarkup(row_width=1)

    remove_button = InlineKeyboardButton(text='Вилучити', callback_data=f'remove_from_basket')
    pay_order_button = InlineKeyboardButton(text='Замовити онлайн', callback_data='pay_order')
    pay_offline_button = InlineKeyboardButton(text='Замовити офлайн', callback_data='pay_offline')
    back_in_main_menu = InlineKeyboardButton(text='Головне меню', callback_data='Головне меню')

    inline_menu.insert(remove_button)
    inline_menu.insert(pay_order_button)
    inline_menu.insert(pay_offline_button)
    inline_menu.insert(back_in_main_menu)

    return inline_menu


def remove_from_basket(user_id):
    with open(f"basket_base/{user_id}.json", "r") as read_file:
        data = json.load(read_file)
    
    products_array = data.get("dish_list")
    inline_menu = InlineKeyboardMarkup(row_width=2)
    buttons = []

    for item in products_array:
        button = InlineKeyboardButton(text=item, callback_data=f'remove_basket_{item}')
        buttons.append(button)

    inline_menu.add(*buttons)

    return inline_menu
