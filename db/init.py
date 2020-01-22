import sqlite3
from sqlite3 import Error
from migrations import *

def create_connection(db_file):
    conn=None

    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

def migration_run(conn):
    c = conn.cursor()

    migrations = [
        host.host_table()
    ]

    for migration in migrations:
        print("test")
        c.execute(migration)


def db_init(store_choice):

    conn = create_connection(store_choice)

    migration_run(conn)


if __name__ == '__main__':
    db_init('../test.db')

    main()
