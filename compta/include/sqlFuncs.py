import sqlite3
from sqlite3 import Error

def check_table(conn, name):
    table = """ CREATE TABLE IF NOT EXISTS """ + name + """ (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL,
                                    begin_date text,
                                    end_date text
                                ); """
    try:
        c = conn.cursor()
        c.execute(table)
        print ("Database created")
        return 200
    except Error as e:
        print(e)