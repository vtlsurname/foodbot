from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


categories = KeyboardButton(text='Категорії')
basket = KeyboardButton(text='Кошик')
tech_support = KeyboardButton(text='Тех. Підтримка')
settings = KeyboardButton(text='Налаштування')

user_main_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(categories, basket, tech_support)


change_phone = KeyboardButton(text='Змінити телефон')
change_home = KeyboardButton(text='Змінити адресу доставки')

settings_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(change_phone, change_home)
