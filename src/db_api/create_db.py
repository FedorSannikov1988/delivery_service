"""
Creates database and user to manage database.
"""
import psycopg2


def creating_database_for_app(host_server: str, port_server: str,
                              user_log_in_server: str, password_log_in_server: str,
                              name_created_database: str, name_manager_created_database: str,
                              password_manager_created_database: str) -> None:
    """
    Сreating a database and an administrator for the database .

    :param host_server: str
    :param port_server: str
    :param user_log_in_server: str
    :param password_log_in_server: str
    :param name_created_database: str
    :param name_manager_created_database: str
    :param password_manager_created_database: str
    :return: None
    """
    host = host_server
    port = port_server
    user = user_log_in_server
    password = password_log_in_server

    connection = psycopg2.connect(
        host=host,
        port=port,
        user=user,
        password=password
    )

    connection.autocommit = True

    cursor = connection.cursor()

    sql_create_database = \
        f"CREATE DATABASE {name_created_database};"
    sql_create_user_for_database = \
        f"CREATE USER {name_manager_created_database} WITH PASSWORD '{password_manager_created_database}';"
    give_privileges_user_for_database = \
        f"GRANT ALL PRIVILEGES ON DATABASE {name_created_database} TO {name_manager_created_database};"

    cursor.execute(sql_create_database)
    cursor.execute(sql_create_user_for_database)
    cursor.execute(give_privileges_user_for_database)

    cursor.close()
    connection.close()
