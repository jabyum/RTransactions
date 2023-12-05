import sqlite3
from datetime import datetime
connection = sqlite3.connect("rt.db")
sql = connection.cursor()
sql.execute("CREATE TABLE IF NOT EXISTS transactions (number INTEGER PRIMARY KEY AUTOINCREMENT, "
            "user_id INTEGER, money TEXT, cardnum TEXT, user_reg_date DATETIME);")
sql.execute("CREATE TABLE IF NOT EXISTS all_users (tg_id INTEGER, user_reg_date DATETIME);")
sql.execute("CREATE TABLE IF NOT EXISTS actual (cardnumber TEXT, reg_date DATETIME);")
connection.commit()

def reg_user(user_id):
    connection = sqlite3.connect("rt.db")
    sql = connection.cursor()
    sql.execute("INSERT INTO all_users (tg_id, user_reg_date) "
                "VALUES (?, ?);", (user_id, datetime.now()))
    connection.commit()
def reg_card(new_card):
    connection = sqlite3.connect("rt.db")
    sql = connection.cursor()
    sql.execute("INSERT INTO actual (cardnumber, reg_date) "
                "VALUES (?, ?);", (new_card, datetime.now()))
    connection.commit()
def delete_card():
    connection = sqlite3.connect("rt.db")
    sql = connection.cursor()
    sql.execute("DELETE FROM actual;")
    connection.commit()
def get_card():
    connection = sqlite3.connect("rt.db")
    sql = connection.cursor()
    checker = sql.execute("SELECT cardnumber FROM actual;").fetchone()
    try:
        return checker[0]
    except:
        return checker
def register_transaction(user_id, money, cardnum):
    connection = sqlite3.connect("rt.db")
    sql = connection.cursor()
    sql.execute("INSERT INTO transactions (user_id, money, cardnum, user_reg_date) "
                "VALUES (?, ?, ?, ?);", (user_id, money, cardnum, datetime.now()))
    connection.commit()
def delete_transaction(user_id):
    connection = sqlite3.connect("rt.db")
    sql = connection.cursor()
    sql.execute("DELETE FROM transactions WHERE user_id=?;", (user_id, ))
    connection.commit()
def check(user_id):
    connection = sqlite3.connect("rt.db")
    sql = connection.cursor()
    checker = sql.execute("SELECT user_id FROM transactions WHERE user_id=?;", (user_id, ))
    if checker.fetchone():
        return True
    else:
        return False
def get_user(user_id):
    connection = sqlite3.connect("rt.db")
    sql = connection.cursor()
    checker = sql.execute("SELECT * FROM transactions WHERE user_id=?;", (user_id, )).fetchone()
    return checker
def mailing_all():
    connection = sqlite3.connect("rt.db")
    sql = connection.cursor()
    all_targets = sql.execute("SELECT tg_id FROM all_users;",).fetchall()
    return all_targets

def check_user(user_id):
    connection = sqlite3.connect("rt.db")
    sql = connection.cursor()
    checker = sql.execute("SELECT tg_id FROM all_users WHERE tg_id=?;", (user_id, ))
    if checker.fetchone():
        return True
    else:
        return False