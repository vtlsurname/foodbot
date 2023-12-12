from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


statistic = KeyboardButton(text='Статистика')
back_in_main_menu = KeyboardButton(text='Назад у меню')
dishes = KeyboardButton(text='Налаштування страв')
base_manage = KeyboardButton(text='БД')
team_manage = KeyboardButton(text='Працівники')
orders = KeyboardButton(text='Замовлення')
black_list = KeyboardButton(text='ЧС')
newsletter = KeyboardButton(text='Розсилка')

admin_menu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(statistic, dishes, base_manage, team_manage, black_list, newsletter, orders)


add_new_dish = KeyboardButton(text='Додати нову страву')
delete_dish = KeyboardButton(text='Видалити страву')

add_new_category = KeyboardButton(text='Додати нову категорію')
delete_category = KeyboardButton(text='Видалити категорію')

change_photo = KeyboardButton(text='Змінити фото')
change_price = KeyboardButton(text='Змінити ціну')
change_desc = KeyboardButton(text='Змінити опис')

dishes_menu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(add_new_dish, delete_dish,add_new_category, delete_category, change_photo, change_price, change_desc, back_in_main_menu)


downlad_base = KeyboardButton(text='Завантажити БД')

base_menu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(downlad_base, back_in_main_menu)


add_admin = KeyboardButton(text='Додати адміна')
delete_admin = KeyboardButton(text='Видалити адміна')

add_chef = KeyboardButton(text='Додати кухаря')
delete_chef = KeyboardButton(text='Видалити кухаря')

team_menu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(add_admin, delete_admin, add_chef, delete_chef, back_in_main_menu)

add_in_bl = KeyboardButton(text='Додати до ЧС')
delete_from_bl = KeyboardButton(text='Видалити з ЧС')

bl_menu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(add_in_bl, delete_from_bl, back_in_main_menu)


with_photo = KeyboardButton(text='Розсилка з фото')
without_photo = KeyboardButton(text='Розсилка без фото')

newsletter_menu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(without_photo, with_photo, back_in_main_menu)
