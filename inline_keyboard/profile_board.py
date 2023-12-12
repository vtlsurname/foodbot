from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_profile_menu():
    inline_menu = InlineKeyboardMarkup(row_width=1)

    phone_btn = InlineKeyboardButton(text='Змінити номер телефону', callback_data='Змінити номер телефону')
    back_in_main_menu = InlineKeyboardButton(text='Головне меню', callback_data='Головне меню')
    
    inline_menu.insert(phone_btn)
    inline_menu.insert(back_in_main_menu)

    return inline_menu
