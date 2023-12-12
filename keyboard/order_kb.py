from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import sqlite3


def get_order_board(name):
    db=sqlite3.connect('base.db')
    cur=db.cursor()

    inline_menu = InlineKeyboardMarkup()

    accept_button = InlineKeyboardButton(text='Додоти в кошик', callback_data=f'add_to_basket_{name}')
    inline_menu.insert(accept_button)

    cencel_button = InlineKeyboardButton(text='Відхилити', callback_data=f'cencel_to_basket')
    inline_menu.insert(cencel_button)

    db.commit()
    db.close()

    return inline_menu


def get_dish_info(name):
    db=sqlite3.connect('base.db')
    cur=db.cursor()

    cur.execute(f"SELECT * FROM dishes WHERE name='{name}'")
    dish_info=cur.fetchall()

    price = dish_info[2]
    name = dish_info[1]

    db.commit()
    db.close()

    return name, price
