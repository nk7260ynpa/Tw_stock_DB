from clients import mysql_conn, mysql_conn_db

class MySQLRouter:
    def __init__(self, host, user, password, db_name=None):
        """
        Initialize the MySQLRouter with the given parameters.

        Args:
            host (str): The MySQL host.
            user (str): The MySQL user.
            password (str): The MySQL password.
            db_name (str, optional): The name of the database. Defaults to None.
        """
        self.host = host
        self.user = user
        self.password = password
        self.db_name = db_name
        self.conn = self._build_mysql_conn()
    
    def _build_mysql_conn(self):
        """
        Build a MySQL connection based on the provided parameters.

        Args:
            self.host (str): The MySQL host.
            self.user (str): The MySQL user.
            self.password (str): The MySQL password.
            self.db_name (str, optional): The name of the database. Defaults to None.

        Returns:
            conn: The MySQL connection object.
        """
        if self.db_name:
            conn = mysql_conn_db(self.host, self.user, self.password, self.db_name)
        else:
            conn = mysql_conn(self.host, self.user, self.password)
        return conn

    @property    
    def mysql_conn(self):
        """
        Get the MySQL connection object.

        Returns:
            conn: The MySQL connection object.

        Example:
        >>> Example:
        >>> router = MySQLRouter(host, user, password, db_name)
        >>> conn = router.mysql_conn
        >>> conn.execute("SELECT 1")
        >>> conn.close()
        """
        return self.conn
        