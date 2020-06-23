import sqlite3
from sqlite3 import Error

def check_table(conn):
    table = """ CREATE TABLE IF NOT EXISTS compta (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL,
                                    description text NOT NULL,
                                    amount real NOT NULL,
                                    date text NOT NULL
                                ); """
    user = """ CREATE TABLE IF NOT EXISTS users (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL,
                                    pwd text NOT NULL,
                                    permissions text
                                ); """
    try:
        c = conn.cursor()
        c.execute(table)
        c.execute(user)
        conn.commit()
        print ("Database created")
        return 200
    except Error as e:
        print(e)


def insert_table(conn, tablename, args):
    if (tablename == "compta"):
        table = """ INSERT INTO """ + tablename + """ (name,description,amount,date) VALUES ('""" + args[0] + """','""" + args[1] + """','""" + args[2] + """','""" + args[3] + """'); """
    if (tablename == "users"):
        table = """ INSERT INTO """ + tablename + """ (name,pwd,permissions) VALUES ('""" + args[0] + """','""" + args[1] + """','""" + args[2] + """'); """
    print(table)
    try:
        c = conn.cursor()
        c.execute(table)
        conn.commit()
        return 200
    except Error as e:
        print(e)

def print_table(conn, name):
    table = """ SELECT * FROM """+ name +"""; """
    try:
        c = conn.cursor()
        c.execute(table)
        conn.commit()
        rows = c.fetchall()
        for row in rows:
            print("print_table: Username database: " + str(row))
        return (rows)
    except Error as e:
        print(e)

def delete_row(conn, tablename, id):
    table = """ DELETE FROM """ + tablename + """ WHERE id = """ + str(id) + """; """
    try:
        c = conn.cursor()
        c.execute(table)
        conn.commit()
        return 200
    except Error as e:
        print(e)

def update_row(conn, tablename, name, args):
    try:
        if (tablename == "users"):
            table = """ UPDATE users SET name = '""" + name + """', pwd = '""" + args[0] + """', permissions = '""" + args[1] + """' WHERE name = '""" + name + """'; """
        if (tablename == "compta"):
            table = """ UPDATE compta SET name = '""" + name + """', description = '""" + args[0] + """', amount = '""" + args[1] + """', date = '""" + args[2] + """' WHERE name = '""" + name + """'; """
        c = conn.cursor()
        c.execute(table)
        conn.commit()
        return 200
    except Error as e:
        print(e)