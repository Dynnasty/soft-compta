import sqlite3
from sqlite3 import Error


def init_db():
    conn = None
    try:
        conn = sqlite3.connect("aled.sql")
        print ("I: Connection to database established")
        return (conn)
    except Error as e:
        print(e)