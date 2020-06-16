import sqlite3
from sqlite3 import Error


def init_db():
    conn = None
    try:
        conn = sqlite3.connect("db.sql")
        print(sqlite3.version)
        return (conn)
    except Error as e:
        print(e)