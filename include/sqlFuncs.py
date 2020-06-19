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
        return (rows)
    except Error as e:
        print(e)
