def host_table():

    # Declare database create statment
    host_table_sql = """CREATE TABLE IF NOT EXISTS hosts (
        id integer PRIMARY KEY,
        ip text NOT NULL,
        created_at timestamp
        updated_at timestamp
    );"""

    return host_table_sql
