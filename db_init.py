import sqlite3


def open():
    conn = sqlite3.connect("mydatabase.db")  # или :memory: чтобы сохранить в RAM
    return conn

conn = open()
cursor = conn.cursor()
cursor.execute("""CREATE TABLE user_settings
               (username text, password text, user_id integer)
           """)

conn.execute("""CREATE TABLE tasks
                  (target_user text, status text, chat_id integer,user_id integer)
               """)