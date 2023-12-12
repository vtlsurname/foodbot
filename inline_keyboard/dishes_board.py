from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import sqlite3


def get_categories_menu():
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM dishes_categories')
    data = cursor.fetchall()

    menu_items = []
    for name in data:
        menu_items.append(name[0])

    # print(menu_items)

    inline_menu = InlineKeyboardMarkup(row_width=2)
    buttons = []
    for item in menu_items:
        button = InlineKeyboardButton(text=item, callback_data=f'food_categori_{item}')
        buttons.append(button)

    back_in_main_menu = InlineKeyboardButton(text='Головне меню', callback_data='Головне меню')
    buttons.append(back_in_main_menu)

    inline_menu.add(*buttons) # for make dynamic menu before button name you need write (example: *button)

    return inline_menu


def get_dishes_menu(categoria):
    db=sqlite3.connect('base.db')
    cur=db.cursor()

    cur.execute(f"SELECT * FROM dishes WHERE categoria='{categoria}'")
    data = cur.fetchall()

    menu_categories = []
    menu_items = []
    for name in data:
        menu_items.append(name[1])
    
    inline_menu = InlineKeyboardMarkup(row_width=2)
    buttons = []
    for item in menu_items:
        button = InlineKeyboardButton(text=item, callback_data=f'food_{item}')
        buttons.append(button)
    back_in_main_menu = InlineKeyboardButton(text='Головне меню', callback_data='Головне меню')
    buttons.append(back_in_main_menu)

    inline_menu.add(*buttons) # for make dynamic menu before button name you need write *(example: *button)

    db.commit()
    db.close()

    return inline_menu


def get_categories_menu_for_adding_new_dish():
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM dishes_categories')
    data = cursor.fetchall()

    menu_items = []
    for name in data:
        menu_items.append(name[0])

    # print(menu_items)

    inline_menu = InlineKeyboardMarkup(row_width=2)
    buttons = []
    for item in menu_items:
        button = InlineKeyboardButton(text=item, callback_data=f'new_food_categori_{item}')
        buttons.append(button)

    # back_in_main_menu = InlineKeyboardButton(text='У адмін меню', callback_data='У адмін меню')
    # buttons.append(back_in_main_menu)

    inline_menu.add(*buttons) # for make dynamic menu before button name you need write (example: *button)

    return inline_menu


def get_categories_menu_for_delete_dish():
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM dishes_categories')
    data = cursor.fetchall()

    menu_items = []
    for name in data:
        menu_items.append(name[0])

    # print(menu_items)

    inline_menu = InlineKeyboardMarkup(row_width=2)
    buttons = []
    for item in menu_items:
        button = InlineKeyboardButton(text=item, callback_data=f'delete_food_categori_{item}')
        buttons.append(button)

    # back_in_main_menu = InlineKeyboardButton(text='У адмін меню', callback_data='У адмін меню')
    # buttons.append(back_in_main_menu)

    inline_menu.add(*buttons) # for make dynamic menu before button name you need write (example: *button)

    return inline_menu


def get_dishes_menu_for_delete(categoria):
    db=sqlite3.connect('base.db')
    cur=db.cursor()

    cur.execute(f"SELECT * FROM dishes WHERE categoria='{categoria}'")
    data = cur.fetchall()

    menu_categories = []
    menu_items = []
    for name in data:
        menu_items.append(name[1])
    
    inline_menu = InlineKeyboardMarkup(row_width=2)
    buttons = []
    for item in menu_items:
        button = InlineKeyboardButton(text=item, callback_data=f'delete_food_{item}')
        buttons.append(button)
    back_in_main_menu = InlineKeyboardButton(text='Головне меню', callback_data='Головне меню')
    buttons.append(back_in_main_menu)

    inline_menu.add(*buttons) # for make dynamic menu before button name you need write *(example: *button)

    db.commit()
    db.close()

    return inline_menu


def categories_menu_for_delete_cat():
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM dishes_categories')
    data = cursor.fetchall()

    menu_items = []
    for name in data:
        menu_items.append(name[0])

    # print(menu_items)

    inline_menu = InlineKeyboardMarkup(row_width=2)
    buttons = []
    for item in menu_items:
        button = InlineKeyboardButton(text=item, callback_data=f'delete_categori_{item}')
        buttons.append(button)

    # back_in_main_menu = InlineKeyboardButton(text='У адмін меню', callback_data='У адмін меню')
    # buttons.append(back_in_main_menu)

    inline_menu.add(*buttons) # for make dynamic menu before button name you need write (example: *button)

    return inline_menu


def get_categories_menu_for_edit_photo():
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM dishes_categories')
    data = cursor.fetchall()

    menu_items = []
    for name in data:
        menu_items.append(name[0])

    # print(menu_items)

    inline_menu = InlineKeyboardMarkup(row_width=2)
    buttons = []
    for item in menu_items:
        button = InlineKeyboardButton(text=item, callback_data=f'edit_photo_food_categori_{item}')
        buttons.append(button)

    # back_in_main_menu = InlineKeyboardButton(text='У адмін меню', callback_data='У адмін меню')
    # buttons.append(back_in_main_menu)

    inline_menu.add(*buttons) # for make dynamic menu before button name you need write (example: *button)

    return inline_menu


def get_dishes_menu_for_edit_photo(categoria):
    db=sqlite3.connect('base.db')
    cur=db.cursor()

    cur.execute(f"SELECT * FROM dishes WHERE categoria='{categoria}'")
    data = cur.fetchall()

    menu_categories = []
    menu_items = []
    for name in data:
        menu_items.append(name[1])
    
    inline_menu = InlineKeyboardMarkup(row_width=2)
    buttons = []
    for item in menu_items:
        button = InlineKeyboardButton(text=item, callback_data=f'edit_photo_food_{item}')
        buttons.append(button)
    back_in_main_menu = InlineKeyboardButton(text='Головне меню', callback_data='Головне меню')
    buttons.append(back_in_main_menu)

    inline_menu.add(*buttons) # for make dynamic menu before button name you need write *(example: *button)

    db.commit()
    db.close()

    return inline_menu


#--- EDIT PRICE ---
def get_categories_menu_for_edit_price():
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM dishes_categories')
    data = cursor.fetchall()

    menu_items = []
    for name in data:
        menu_items.append(name[0])


    inline_menu = InlineKeyboardMarkup(row_width=2)
    buttons = []
    for item in menu_items:
        button = InlineKeyboardButton(text=item, callback_data=f'edit_price_food_categori_{item}')
        buttons.append(button)

    inline_menu.add(*buttons)

    return inline_menu


def get_dishes_menu_for_edit_price(categoria):
    db=sqlite3.connect('base.db')
    cur=db.cursor()

    cur.execute(f"SELECT * FROM dishes WHERE categoria='{categoria}'")
    data = cur.fetchall()

    menu_categories = []
    menu_items = []
    for name in data:
        menu_items.append(name[1])
    
    inline_menu = InlineKeyboardMarkup(row_width=2)
    buttons = []
    for item in menu_items:
        button = InlineKeyboardButton(text=item, callback_data=f'edit_price_food_{item}')
        buttons.append(button)
    back_in_main_menu = InlineKeyboardButton(text='Головне меню', callback_data='Головне меню')
    buttons.append(back_in_main_menu)

    inline_menu.add(*buttons) 

    db.commit()
    db.close()

    return inline_menu


#--- EDIT DESCRIPTION---
def get_categories_menu_for_edit_desc():
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM dishes_categories')
    data = cursor.fetchall()

    menu_items = []
    for name in data:
        menu_items.append(name[0])


    inline_menu = InlineKeyboardMarkup(row_width=2)
    buttons = []
    for item in menu_items:
        button = InlineKeyboardButton(text=item, callback_data=f'edit_desc_food_categori_{item}')
        buttons.append(button)

    inline_menu.add(*buttons)

    return inline_menu

def get_dishes_menu_for_edit_desc(categoria):
    db=sqlite3.connect('base.db')
    cur=db.cursor()

    cur.execute(f"SELECT * FROM dishes WHERE categoria='{categoria}'")
    data = cur.fetchall()

    menu_categories = []
    menu_items = []
    for name in data:
        menu_items.append(name[1])
    
    inline_menu = InlineKeyboardMarkup(row_width=2)
    buttons = []
    for item in menu_items:
        button = InlineKeyboardButton(text=item, callback_data=f'edit_desc_food_{item}')
        buttons.append(button)
    back_in_main_menu = InlineKeyboardButton(text='Головне меню', callback_data='Головне меню')
    buttons.append(back_in_main_menu)

    inline_menu.add(*buttons) 

    db.commit()
    db.close()

    return inline_menu
