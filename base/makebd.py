import sqlite3

def create_new_table():
    db = sqlite3.connect('base.db')
    cur = db.cursor()

    cur.execute("CREATE TABLE orders (user_id integer, dish_order text)")
    db.commit()

    # cur.execute("INSERT INTO dishes_categories VALUES (723898920)")

    db.commit()
    db.close()
create_new_table()

def add_something():
    db = sqlite3.connect('base.db')
    cur = db.cursor()

    cur.execute("INSERT INTO dishes_categories VALUES('Суші')")

    db.commit()
    db.close()
# add_something()


# def get_users_ids():
#     db = sqlite3.connect('base.db')
#     cur = db.cursor()

#     cur.execute("SELECT user_id FROM users_bd")
#     dirrt_users = cur.fetchall()
#     clean_users = []

#     for user in dirrt_users:
#         clean_users.append(user[0])

#     db.commit()
#     db.close()

#     return clean_users

#many users in base>
# def get_stat():
#     db = sqlite3.connect('base.db')
#     cur = db.cursor()

#     cur.execute("SELECT user_id FROM users_bd")
#     dirrt_users = cur.fetchall()

#     db.commit()
#     db.close()

#     many_users = len(dirrt_users)
#     return many_users

# get_stat()

def delete_all():
    db=sqlite3.connect("base.db")
    cur=db.cursor()

    cur.execute("DELETE FROM dishes_categories")

    db.commit()
    db.close()
# delete_all()

def delete_one():
    db=sqlite3.connect("base.db")
    cur=db.cursor()

    cur.execute("DELETE FROM dishes_categories WHERE categories='Суші'")

    db.commit()
    db.close()
# delete_one()


def delete_table():
    db=sqlite3.connect('base.db')
    cur=db.cursor()

    cur.execute("DROP TABLE test")

    db.cursor()
    db.close()
# delete_table()


def add_new_column():
    conn = sqlite3.connect("base.db")
    cursor = conn.cursor()

    cursor.execute("ALTER TABLE dishes ADD COLUMN description TEXT")

    conn.commit()
    conn.close()
#add_new_column()