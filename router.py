from clients import mysql_conn, mysql_conn_db
from sqlalchemy import text

class MySQLRouter:
    def __init__(self, host, user, password, db_name=None):
        self.host = host
        self.user = user
        self.password = password
        self.db_name = db_name
        self.conn = self.build_mysql_conn()
    
    def build_mysql_conn(self):
        if self.db_name:
            conn = mysql_conn_db(self.host, self.user, self.password, self.db_name)
        else:
            conn = mysql_conn(self.host, self.user, self.password)
        return conn

    @property    
    def mysql_conn(self):
        return self.conn
        