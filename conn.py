from mysql.connector import Error

import mysql.connector

def connect_server(host, user, pwd):
    """
    Establish a connection to a MySQL server without specifying a database.

    :param host: The hostname or IP address of the MySQL server.
    :param user: The username to use for authentication.
    :param pwd: The password to use for authentication.
    :return: A MySQL connection object or None if the connection fails.
    """
    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=pwd
        )
        if conn.is_connected():
            print("Connected to MySQL server.")
            return conn
    except Error as e:
        raise Exception(f"SQL Server Connection Error: {e}")

def connect_db(host, user, pwd, db):
    """
    Establish a connection to a MySQL database.

    :param host: The hostname or IP address of the MySQL server.
    :param user: The username to use for authentication.
    :param pwd: The password to use for authentication.
    :param db: The name of the database to connect to.
    :return: A MySQL connection object or None if the connection fails.
    """
    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=pwd,
            database=db
        )
        if conn.is_connected():
            print("Connected to MySQL database.")
            return conn
    except Error as e:
        raise Exception(f"SQL Connection Error: {e}")