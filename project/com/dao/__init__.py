import sqlite3

def conn_db():
    return sqlite3.connect('hasoc.db', check_same_thread=False)
