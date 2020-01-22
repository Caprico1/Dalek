def scan_table():

    scan_table_sql = """
    CREATE TABLE IF NOT EXISTS scans(
        id integer,
        host_id string

    )
    """

    return scan_table_sql
