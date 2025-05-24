import os
from abc import ABC, abstractmethod
import re

from sqlalchemy import text

class BuildEmptyDB():    
    def __init__(self, sql_file_path):
        self.sql_file_path = sql_file_path
        self.sql = self.read_sql_file()
        self.db_name = self.get_db_name()

    def read_sql_file(self):
        with open(self.sql_file_path, 'r') as file:
            sql = file.read()
        return sql

    def get_db_name(self):
        start = self.sql.find("`") + 1
        end = self.sql.find("`", start)
        return self.sql[start:end]
    
    def check_db_exists(self, conn):
        query = text(f"SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = '{self.db_name}'")
        results = conn.execute(query)
        rows = results.fetchall()
        if len(rows) > 0:
            return True
        else:
            return False
        
    def build(self, conn_server):
        if not self.check_db_exists(conn_server):
            conn_server.execute(text(self.sql))
            print(f"Database '{self.db_name}' created successfully.")
        else:
            print(f"Database '{self.db_name}' already exists.")
        conn_server.close()


class BaseBuildTABLE(ABC):
    def __init__(self):
        folder_name = re.search(r'Build(.*?)TABLE', self.__class__.__name__).group(1)
        table_name = re.search(r'TABLE(.*)', self.__class__.__name__).group(1)  
        self.sql_file_path = os.path.join("build_DB", folder_name+"_sql", f"{table_name}.sql")
        self.sql = self.read_sql_file()
        self.table_name = table_name
        
    def read_sql_file(self):
        with open(self.sql_file_path, 'r') as file:
            sql = file.read()
        return sql
        
    def check_table_exists(self, conn):
        """
        Check if the table already exists in the database.
        """
        query = text(f"SELECT COUNT(*) FROM information_schema.tables WHERE table_name = '{self.table_name}'")
        result = conn.execute(query)
        count = result.fetchone()[0]
        return count > 0
    
    @abstractmethod
    def post_process(self):
        pass
    
    def build(self, conn):
        if not self.check_table_exists(conn):
            conn.execute(text(self.sql))
            self.post_process()
            print(f"Table '{self.table_name}' created successfully.")
        else:
            print(f"Table '{self.table_name}' already exists.")

class BaseBuild(ABC):
    def __init__(self, typeclass, name):
        self.typeclass = typeclass
        self.name = name
        self.folder = os.path.join("build_DB")

    def build_db(self, conn_server):
        sql_path = os.path.join(self.folder, f"{self.name}_sql", "db.sql")
        build_obj = BuildEmptyDB(sql_path)
        build_obj.build(conn_server)
    
    def build_table(self, conn):
        for subclass in self.typeclass.__subclasses__():
            sql_path = os.path.join(self.folder, f"{self.name}_sql", f"{subclass.__name__}.sql")
            build_obj = subclass()
            build_obj.build(conn)
    