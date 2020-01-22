def port_table():

    port_table_sql = """
    CREATE TABLE IF NOT EXISTS port(
        id integer PRIMARY KEY,
        port_number integer NOT NULL,
        protocol String,
    );
    """

    return port_table_sql

def port_host_table():

    port_to_host_sql = """
    CREATE TABLE IF NOT EXISTS host_port(
        host_id integer,
        port_id integer,
        FOREIGN KEY(host_id) REFERENCES host(id),
        FOREIGN KEY(port_id) REFERENCES port(id)
    );
    """

    return port_to_host_sql
