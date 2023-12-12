import sqlite3, os


def is_dish_in_bd(dish_name):
    db=sqlite3.connect('base.db')
    cur=db.cursor()
    
    cur.execute("SELECT name FROM dishes")
    items = cur.fetchall()
    
    for item in items:
        if item[0] == dish_name:
            return 1
        
        return 0
    
    db.commit()
    db.close()


def add_new_dish_in_bd(categori, dish_name, price, description, img_url):
    db=sqlite3.connect('base.db')
    cur=db.cursor()

    cur.execute(f"INSERT INTO dishes VALUES('{categori}', '{dish_name}', {price}, '{img_url}', '{description}')")
    
    db.commit()
    db.close()


def delete_dish(dish_name):
    db=sqlite3.connect('base.db')
    cur=db.cursor()

    cur.execute(f"DELETE FROM dishes WHERE name='{dish_name}'")

    try:
        os.remove(path=f'images/{dish_name}.png')
    except Exception as ex:
        print(ex)

    db.commit()
    db.close()


def is_column_in_bd(table_name, column_name):
    conn = sqlite3.connect('base.db')

    cursor = conn.cursor()
    cursor.execute(f"PRAGMA TABLE_INFO({table_name})")

    columns = [row[1] for row in cursor]

    if column_name in columns:
        conn.close()
        return 0
    else:
        conn.close()
        return 1


def change_dish_description(dish_name, new_desc):
    db = sqlite3.connect('base.db')
    cur = db.cursor()
    
    try:
        cur.execute(f"UPDATE dishes SET description='{new_desc}' WHERE name='{dish_name}'")
        
        db.commit()
        db.close()

        return 'Опис було успішно змінено!'
        
    except Exception as ex:
        db.commit()
        db.close()
        return ex
