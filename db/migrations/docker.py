
def docker_table():
    docker_table_sql = """
    CREATE TABLE IF NOT EXISTS docker(
        id integer PRIMARY KEY,
        image string,
        id string,
        command text,
        created timestamp,
        name text,
        ports integer,
        status text,
    );
    """

    return docker_table_sql

def docker_components():

    docker_components_sql = """
        CREATE TABLE IF NOT EXISTS docker_component(
            id integer PRIMARY KEY,
            name string,
            details text,
            experitmental text,
            os string,
            minAPIVersion string,
            KernelVersion string,
            goVersion string,
            gitCommit string,
            buildTime string,
            apiVersion string,
            arch string
        );
    """

    return docker_components_sql
