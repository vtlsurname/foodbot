from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_main_menu():
    inline_menu = InlineKeyboardMarkup(row_width=2)

    catefori_btn = InlineKeyboardButton(text='📊Категорії', callback_data='Категорії')
    basket_btn = InlineKeyboardButton(text='🗑️Кошик', callback_data='Кошик')
    profile_btn = InlineKeyboardButton(text='👤Профіль', callback_data='Профіль')

    inline_menu.insert(catefori_btn)
    inline_menu.insert(basket_btn)
    inline_menu.insert(profile_btn)

    return inline_menu


def back_in_menu():
    inline_menu = InlineKeyboardMarkup(row_width=2)
    back_in_main_menu = InlineKeyboardButton(text='Головне меню', callback_data='Головне меню')
    inline_menu.insert(back_in_main_menu)
    
    return inline_menu
