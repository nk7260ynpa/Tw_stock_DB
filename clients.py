from sqlalchemy import create_engine

def mysql_conn(host, user, password):
    """
    Create a MySQL connection without specifying a database.
    Args:
        host (str): The MySQL host.
        user (str): The MySQL user.
        password (str): The MySQL password.

    Returns:
        conn: The MySQL connection object.

    Example:
    >>> conn = mysql_conn("localhist:3306", "root", "password")
    >>> conn.execute("SELECT 1")
    >>> conn.close()
    """
    address = f"mysql+pymysql://{user}:{password}@{host}"
    engine = create_engine(address)
    conn = engine.connect()
    return conn

def mysql_conn_db(host, user, password, db_name):
    """
    Create a MySQL connection without specifying a database.
    Args:
        host (str): The MySQL host.
        user (str): The MySQL user.
        password (str): The MySQL password.

    Returns:
        conn: The MySQL connection object.

    Example:
    >>> conn = mysql_conn("localhist:3306", "root", "password", "TWSE")
    >>> conn.execute("SELECT 1")
    >>> conn.close()
    """
    address = f"mysql+pymysql://{user}:{password}@{host}/{db_name}"
    engine = create_engine(address)
    conn = engine.connect()
    return conn
