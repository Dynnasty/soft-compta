import sqlite3
from sqlite3 import Error

def check_table(conn):
    table = """ CREATE TABLE IF NOT EXISTS compta (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL,
                                    description text NOT NULL,
                                    amount real NOT NULL,
                                    date text NOT NULL,
                                    recieptpath text,
                                    state text NOT NULL

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
        print ("I: Database formatted and ready to use")
        return 200
    except Error as e:
        print(e)


def insert_table(conn, tablename, args):
    if (tablename == "compta"):
        try:
            table = """ INSERT INTO """ + tablename + """ (name,description,amount,date, recieptpath,state) VALUES ('""" + args[0] + """','""" + args[1] + """','""" + args[2] + """','""" + args[3] + """', '""" + args[4] + """','Pending'); """
        except IndexError:
            print("No file provided! Inserting without filepath")
            table = """ INSERT INTO """ + tablename + """ (name,description,amount,date, recieptpath,state) VALUES ('""" + args[0] + """','""" + args[1] + """','""" + args[2] + """','""" + args[3] + """', 'NULL','Pending'); """

    if (tablename == "users"):
        table = """ INSERT INTO """ + tablename + """ (name,pwd,permissions) VALUES ('""" + args[0] + """','""" + args[1] + """','""" + args[2] + """'); """
    print("I: Trying the following requqest:")
    print (table)
    try:
        c = conn.cursor()
        c.execute(table)
        conn.commit()
        print("I: Entry inserted into table: " + tablename)
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
        print ("I: Content of: " + name + " successfully fetched")
        return (rows)
    except Error as e:
        print(e)

def delete_row(conn, tablename, id):
    table = """ DELETE FROM """ + tablename + """ WHERE id = """ + str(id) + """; """
    try:
        c = conn.cursor()
        c.execute(table)
        conn.commit()
        print ("I: Entry deleted successfully")
        return 200
    except Error as e:
        print(e)

def update_row(conn, tablename, name, args):
    try:
        if (tablename == "users"):
            table = """ UPDATE users SET name = '""" + name + """', pwd = '""" + args[0] + """', permissions = '""" + args[1] + """' WHERE name = '""" + name + """'; """
        if (tablename == "compta"):
            table = """ UPDATE compta SET name = '""" + args[5] + """', description = '""" + args[0] + """', amount = '""" + args[1] + """', date = '""" + args[2] + """',  recieptpath = '""" + args[3] + """' ,state = '""" + args[4] + """' WHERE id = '""" + str(name) + """'; """
        c = conn.cursor()
        c.execute(table)
        conn.commit()
        print ("I: Entry: " + name + " updated successfully")
    except Error as e:
        print(e)