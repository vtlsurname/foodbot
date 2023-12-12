import sqlite3, json, os
from typing import List, Tuple
from datetime import datetime


def is_user_in_bd(user_id):
    db = sqlite3.connect("base.db")
    cur = db.cursor()

    cur.execute("SELECT user_id FROM users_info_bd")
    users = cur.fetchall()
    
    for user in users:
        if user_id == user[0]:
            return True

    db.commit()
    db.close()


def add_user_in_bd(user_id):
    db = sqlite3.connect("base.db")
    cur = db.cursor()

    cur.execute(f"INSERT INTO users_info_bd VALUES({user_id}, 0, NULL)")

    db.commit()
    db.close()


def add_new_column():
    db = sqlite3.connect("base.db")
    cur=db.cursor()

    cur.execute(f"ALTER TABLE admins ADD COLUMN admin_name text")

    db.commit()
    db.close()
# add_new_column()

def delete_user(user_id):
    db = sqlite3.connect("base.db")
    cur = db.cursor()

    cur.execute(f"DELETE FROM users_info_bd WHERE user_id={user_id}")

    db.commit()
    db.close()


def update_user_phone(user_id, user_phone):
    db=sqlite3.connect("base.db")
    cur=db.cursor()

    try:
        cur.execute(f"UPDATE users_info_bd SET phone='{user_phone}' WHERE user_id={user_id}")
        
        db.commit()
        db.close()
        return True
    except Exception as ex:
        print(ex)

        db.commit()
        db.close()
        return False
# update_user_phone(user_id=723898920, user_phone='+380957506458')

# функция для получения и назначение нового messege_id потомучто у каждого пользователя он разный и его нужно изменять
def get_message_id(user_id):
    db=sqlite3.connect('base.db')
    cur=db.cursor()
    try:
        cur.execute(f"SELECT * FROM message_id WHERE user_id={user_id}")
        user_message_id = cur.fetchall()[0]
    except:
        return 0

    db.commit()
    db.close()

    return int(user_message_id[1])
# get_message_id(user_id=7238989202)

def set_message_id(user_id, message_id):
    db=sqlite3.connect('base.db')
    cur=db.cursor()


    cur.execute(f"SELECT * FROM message_id WHERE user_id={user_id}")
    length_arr = len(cur.fetchall())

    if length_arr != 0:
        cur.execute(f"UPDATE message_id SET message_id={message_id} WHERE user_id={user_id}")
        
    else:
        cur.execute(f"INSERT INTO message_id VALUES({user_id}, {message_id})")


    db.commit()
    db.close()
# set_message_id(user_id=7238989202, message_id=228)


def update_basket(user_id, product_name):
    try:
        with open(f"basket_base/{user_id}.json", "r") as read_file:
            last_data = json.load(read_file)
            dish_array = last_data.get('dish_list')
            dish_array.append(product_name)

            new_data = {
                'user_id':user_id,
                'dish_list':dish_array
            }
            with open(f'basket_base/{user_id}.json', 'w') as write_file:
                json.dump(new_data, write_file)

    except Exception as ex:
        with open(f'basket_base/{user_id}.json', 'w') as write_file:
            data = {
                'user_id':user_id,
                'dish_list':[product_name]
            }
            json.dump(data, write_file)


def make_description_order(user_id):
    message_text='У вашому кошику є:\n\n'

    with open(f"basket_base/{user_id}.json", "r") as read_file:
        data = json.load(read_file)
    
    summ=0
    basket_array = data.get("dish_list")
    for item in basket_array:
        db=sqlite3.connect('base.db')
        cur=db.cursor()

        cur.execute(f"SELECT price FROM dishes WHERE name='{item}'")
        summ += cur.fetchall()[0][0]
        message_text+=f'{item}, '

        db.commit()
        db.close()
    message_text += f"Сумма до сплати: {summ} грн."

    return message_text


def get_order_summ(user_id):
    with open(f"basket_base/{user_id}.json", "r") as read_file:
        data = json.load(read_file)
    
    basket_array = data.get("dish_list")
    summ=0
    for item in basket_array:
        db=sqlite3.connect('base.db')
        cur=db.cursor()

        cur.execute(f"SELECT price FROM dishes WHERE name='{item}'")
        summ += cur.fetchall()[0][0]

        db.commit()
        db.close()
 
    return int(summ)


def del_dish_from_bskt(user_id, product_name):
    with open(f"basket_base/{user_id}.json", "r") as read_file:
        data = json.load(read_file)
    dish_list = data.get("dish_list")

    dish_list.remove(product_name)

    data={
        'user_id':user_id,
        'dish_list':dish_list
    }

    with open(f'basket_base/{user_id}.json', 'w') as write_file:
        json.dump(data, write_file)


def add_new_categori(categori_name):
    db=sqlite3.connect('base.db')
    cur=db.cursor()

    cur.execute(f"INSERT INTO dishes_categories VALUES('{categori_name}')")

    db.commit()
    db.close()

def delete_categori(categori_name):
    db=sqlite3.connect('base.db')
    cur=db.cursor()

    try:
        cur.execute(f"DELETE FROM dishes_categories WHERE categories='{categori_name}'")
        db.commit()
    except Exception as ex:
        print(ex)
    
    try:
        cur.execute(f"DELETE FROM dishes WHERE categoria='{categori_name}'")
    except Exception as ex:
        print(ex)

    db.commit()
    db.close()


def check_clean_base(user_id):
    try:
        with open(f'basket_base/{user_id}.json', 'r') as f:
            data = json.load(f)
    except:
        return 'Ваш кошик пустий.'
        
    dirt_dish_array = data.get('dish_list')
    clean_dish_array = []
    
    for item in dirt_dish_array:
        db=sqlite3.connect('base.db')
        cur=db.cursor()
        
        try:
            cur.execute(f"SELECT name FROM dishes WHERE name='{item}'")
            clean_dish_array.append(cur.fetchone()[0])
        except:
            pass
        
        db.commit()
        db.close()
    
    data = {
        'user_id':user_id,
        'dish_list':clean_dish_array
    }
    
    with open(f'basket_base/{user_id}.json', 'w') as write_file:
        json.dump(data, write_file)


def make_basket_message(user_id):
    
    check_clean_base(user_id)
    
    message_text='У вашому кошику є:\n\n'
    try:
        with open(f'basket_base/{user_id}.json', 'r') as f:
            data = json.load(f)
    except:
        return 'Ваш кошик пустий.'
    
    clean_dish_array=data.get('dish_list')
    if len(clean_dish_array) == 0:
        return 'Ваш кошик пустий.'
    
    counts = {}
    sum = 0
    for item in clean_dish_array:
        db=sqlite3.connect('base.db')
        cur=db.cursor()
        
        cur.execute(f"SELECT price FROM dishes WHERE name='{item}'")
        sum+=cur.fetchone()[0]
        
        db.commit()
        db.close()

    for item in clean_dish_array:
        if item in counts:
            counts[item] += 1
        else:
            counts[item] = 1
    
    for i in counts:
        message_text += f'{i}  <b>X{counts[i]}</b>\n'

    message_text += "\n"
    message_text += f"Сумма до сплати: {sum} грн."
    
    return message_text

def bot_statistic():
    db=sqlite3.connect('base.db')
    cur=db.cursor()
    
    cur.execute("SELECT * FROM users_info_bd")
    users = len(cur.fetchall())
    
    db.commit()
    db.close()
    
    return users
    
# bot_statistic()

def profile_message(user_id):
    db=sqlite3.connect('base.db')
    cur=db.cursor()
    message_text = 'Ваш профіль:\n'

    cur.execute(f"SELECT * FROM users_info_bd WHERE user_id={user_id}")
    user_info = cur.fetchall()[0]
    
    many_purchases = user_info[1]
    user_phone = user_info[2]

    message_text+=f'\nКількість замовлень: {many_purchases}\nНомер телефону: {user_phone}'

    db.commit()
    db.close()
    return message_text


def change_price(dish_name ,new_price):
    db = sqlite3.connect('base.db')
    cur = db.cursor()

    cur.execute(f"UPDATE dishes SET price={new_price} WHERE name='{dish_name}'")

    db.commit()
    db.close()


def make_dish_preview_message(dish_name):
    db = sqlite3.connect('base.db')
    cur = db.cursor()

    cur.execute(f"SELECT * FROM dishes WHERE name='{dish_name}'")
    dish_data = cur.fetchall()[0]

    name = dish_data[1]
    description = dish_data[4]
    price = dish_data[2]

    message_text = f'Назва: {name}\n\nОпис:\n{description}\n\nЦіна: {price}грн.'


    db.commit()
    db.close()

    return message_text

def add_new_admin_func(user_id, user_name):
    # Connect to the database
    conn = sqlite3.connect('base.db')
    c = conn.cursor()

    # Check if the user_id or user_name already exist in the admins table
    c.execute("SELECT COUNT(*) FROM admins WHERE user_id = ? OR admin_name = ?", (user_id, user_name))
    result = c.fetchone()[0]
    if result > 0:
        # Close the database connection
        conn.close()
        return "User ID or user name already exists in the database."

    # Insert the new row into the admins table
    c.execute("INSERT INTO admins (user_id, admin_name) VALUES (?, ?)", (user_id, user_name))
    conn.commit()

    # Close the database connection
    conn.close()

    return "До бази даних додано нового адміністратора."


def get_admin_list_from_database():
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()

    # Select all rows from the admins table and fetch the results
    cursor.execute("SELECT admin_name FROM admins")
    admin_list = [row[0] for row in cursor.fetchall()]

    conn.close()
    return admin_list


def delete_admin_from_database(admin_name):
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()

    # Delete the row in the admins table that matches the given admin name
    cursor.execute("DELETE FROM admins WHERE admin_name = ?", (admin_name,))
    conn.commit()

    conn.close()


def get_admin_ids_from_database():
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT user_id FROM admins')
    admin_ids = [row[0] for row in cursor.fetchall()]
    conn.close()
    
    return admin_ids


def get_chef_list_from_database():
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()

    cursor.execute("SELECT user_name FROM chefs")
    chef_list = [row[0] for row in cursor.fetchall()]

    conn.close()

    return chef_list


def delete_chef_from_database(chef_name):
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM chefs WHERE user_name = ?", (chef_name,))
    conn.commit()

    conn.close()


def add_new_chef_func(user_id, user_name):
    conn = sqlite3.connect('base.db')
    c = conn.cursor()

    c.execute("SELECT COUNT(*) FROM chefs WHERE user_id = ? OR user_name = ?", (user_id, user_name))
    result = c.fetchone()[0]
    if result > 0:
        conn.close()
        return "User ID or user name already exists in the database."

    c.execute("INSERT INTO chefs (user_id, user_name) VALUES (?, ?)", (user_id, user_name))
    conn.commit()

    conn.close()

    return "New chef added to the database."


def save_order_to_db(user_id):
    # Открытие json файла с корзиной пользователя
    file_path = f"basket_base/{user_id}.json"
    with open(file_path, "r") as f:
        basket_data = json.load(f)
        dish_list = basket_data["dish_list"]

    # Проверка наличия активного заказа для пользователя
    conn = sqlite3.connect("base.db")
    cur = conn.cursor()
    cur.execute("SELECT user_id FROM orders WHERE user_id=?", (user_id,))
    existing_order = cur.fetchone()
    if existing_order:
        conn.close()
        return "У вас вже є активне замовлення"

    # Запись заказа в базу данных
    conn = sqlite3.connect("base.db")
    cur = conn.cursor()

    cur.execute("INSERT INTO orders (user_id, dish_order) VALUES (?, ?)", (user_id, ", ".join(dish_list)))

    conn.commit()
    conn.close()

    # Удаление файла json с корзиной пользователя
    os.remove(file_path)

    return 'Замовлення було відправлене адміністратору'


def save_order_to_chef(user_id: int, dish_order: List[str]):
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()

    cursor.execute("INSERT INTO chef_orders (user_id, dish_order) VALUES (?, ?)", (user_id, ", ".join(dish_order)))
    conn.commit()

    cursor.close()
    conn.close()


def delete_order(user_id: int) -> str:
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    try:
        # Удаляем заказ из таблицы orders
        cursor.execute('DELETE FROM orders WHERE user_id = ?', (user_id,))
        conn.commit()
        return "Заказ успешно удален"
    except Exception as e:
        return f"Ошибка при удалении заказа: {e}"
    finally:
        cursor.close()
        conn.close()


def get_order(order_id):
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders WHERE user_id=?", (order_id,))
    order = cursor.fetchone()
    conn.close()
    return order


def get_chef_ids_from_database():
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT user_id FROM chefs')
    chef_ids = [row[0] for row in cursor.fetchall()]
    conn.close()
    
    return chef_ids

def get_chef_orders_from_database() -> List[Tuple[int, str]]:
    with sqlite3.connect("base.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, dish_order FROM chef_orders")
        orders = cursor.fetchall()
        return orders


def get_ukr_time():
    now = datetime.now().strftime("%H:%M")
    return now


def save_order_to_history(chef_id, chef_name, dish_order, time):
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()

    # преобразуем список блюд в строку, разделив запятыми
    dish_order_str = ', '.join(dish_order)

    # записываем данные в таблицу orders_history
    cursor.execute(f"INSERT INTO orders_history (chef_id, chef_name, dish_order, time) VALUES (?, ?, ?, ?)", (chef_id, chef_name, dish_order_str, time))

    # сохраняем изменения в бд
    conn.commit()

    # закрываем соединение
    conn.close()


def get_chef_name(chat_id: int) -> str:
    connection = sqlite3.connect('base.db')
    cursor = connection.cursor()
    cursor.execute(f"SELECT user_name FROM chefs WHERE user_id = {chat_id}")
    result = cursor.fetchone()
    connection.close()
    if result:
        chef_name = result[0]
    else:
        chef_name = "Unknown Chef"
    return chef_name


def get_user_orders(user_id):
    # Подключаемся к базе данных
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()

    # Получаем список заказов пользователя
    cursor.execute('SELECT dish_order FROM chef_orders WHERE user_id = ?', (user_id,))
    user_orders = [row[0] for row in cursor.fetchall()]

    conn.close()

    return user_orders


def delete_user_order(user_id):
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM chef_orders WHERE user_id=?", (user_id,))
    
    conn.commit()
    conn.close()


def get_phone_by_user_id(user_id):
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()

    # получаем телефон пользователя по его user_id
    cursor.execute(f"SELECT phone FROM users_info_bd WHERE user_id='{user_id}'")
    phone = cursor.fetchone()

    # закрываем соединение
    conn.close()

    if phone:
        return phone[0]
    else:
        return None


def get_blacklist_users():
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()

    # Выбираем все user_id из таблицы black_list
    cursor.execute("SELECT user_id FROM black_list")
    rows = cursor.fetchall()

    # Преобразуем полученный список кортежей в список user_id
    users_ids = [row[0] for row in rows]

    conn.close()

    return users_ids


def get_admin_note(order_id: int) -> str:
    with sqlite3.connect("base.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT admin_not FROM chef_orders WHERE user_id = ?", (order_id,))
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            return ""


def increase_user_purchases(user_id):
    with sqlite3.connect("base.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT many_purchases FROM users_info_bd WHERE user_id = ?", (user_id,))
        purchases = cursor.fetchone()[0]
        purchases += 1
        cursor.execute("UPDATE users_info_bd SET many_purchases = ? WHERE user_id = ?", (purchases, user_id))
        conn.commit()
