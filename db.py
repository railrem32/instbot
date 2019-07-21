import sqlite3


def open():
    conn = sqlite3.connect("mydatabase.db")  # или :memory: чтобы сохранить в RAM
    return conn


CONST_STATUS_INPROCESS = "INPROCESS"
CONST_STATUS_FAILED = "FAILED"
CONST_STATUS_FINISHED = "FINISHED"
CONST_STATUS_NEW = "NEW"

# Task
FIELD_STATUS = 'status'
FIELD_USER_ID = 'user_id'
FIELD_CHAT_ID = 'chat_id'
FIELD_TARGET_USER = 'target_user'

# User Setting
FIELD_USERNAME = 'username'
FIELD_PASSWORD = 'password'


# Создание таблицы
# conn = open()
# cursor = conn.cursor()
# cursor.execute("""CREATE TABLE user_settings
#                (username text, password text, user_id integer)
#            """)
#
# conn.execute("""CREATE TABLE tasks
#                   (target_user text, status text, chat_id integer,user_id integer)
#                """)

def create_task(target_user, chat_id, user_id):
    conn = open()
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO tasks
                              VALUES (?, ?, ?,?)""", [target_user, CONST_STATUS_NEW, chat_id, user_id]
                   )
    conn.commit()
    conn.close()


def update_task_status(target_user, user_id, status):
    conn = open()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE tasks 
        SET status = ? 
        WHERE user_id = ? and target_user = ?
        """, [status, user_id, target_user])
    conn.commit()
    conn.close()


def get_first_new_tasks():
    conn = open()
    cursor = conn.cursor()
    sql = "SELECT * FROM tasks WHERE status=?"
    cursor.execute(sql, [(CONST_STATUS_NEW)])
    task = cursor.fetchone()
    conn.close()
    if task is not None:
        return wrapTask(task)
    else:
        return task


def get_task_status(user_id, chat_id, username):
    conn = open()
    cursor = conn.cursor()
    sql = "SELECT * FROM tasks WHERE user_id=? and chat_id=? and target_user=?"
    cursor.execute(sql, [user_id, chat_id, username])
    task = cursor.fetchone()
    conn.close()
    if task is not None:
        return {'target_user': task[0], 'status': task[1], 'chat_id': task[2], 'user_id': task[3]}
    else:
        return task


def get_user_settings(user_id):
    conn = open()
    cursor = conn.cursor()
    sql = "SELECT * FROM user_settings WHERE user_id=?"
    cursor.execute(sql, [(user_id)])
    user = cursor.fetchone()
    conn.close()
    return user


def wrapUser(item):
    return {FIELD_USERNAME: item[0], FIELD_PASSWORD: item[1], FIELD_USER_ID: item[2]}


def set_user_settings(user_id, login, password):
    user = get_user_settings(user_id)
    conn = open()
    cursor = conn.cursor()
    if (user is None):
        cursor.execute("""INSERT INTO user_settings
                          VALUES (?, ?, ?)""", [login, password, user_id]
                       )
    else:
        cursor.execute("""
        UPDATE user_settings 
        SET username = ? ,
        password = ?
        WHERE user_id = ?
        """, [login, password, user_id])
    conn.commit()
    conn.close()
    return user


def wrapTask(item):
    return {FIELD_TARGET_USER: item[0], FIELD_STATUS: item[1], FIELD_CHAT_ID: item[2], FIELD_USER_ID: item[3]}
