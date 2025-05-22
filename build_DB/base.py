import os
from abc import ABC, abstractmethod
import re

from sqlalchemy import text

from build_DB.create_DB import BuildDB

class BaseBuildTABLE(ABC):
    def __init__(self, sql_file_path):
        folder_name = re.search(r'Build(.*?)TABLE', self.__class__.__name__).group(1)
        table_name = re.search(r'TABLE(.*)', self.__class__.__name__).group(1)

  
        self.sql_file_path = os.path.join("build_DB", folder_name+"_sql", f"{table_name}.sql")
        self.sql = self.read_sql_file()
        self.table_name = self.get_table_name()

    def load_sql_path(self):
        sql_folder = re.search(r'Build(.*?)TABLE', self.__class__.__name__).group(1)
        
    def read_sql_file(self):
        with open(self.sql_file, 'r') as file:
            sql = file.read()
        return sql
    
    def get_table_name(self):
        match = re.search(r'CREATE TABLE `.*?`\.`(.*?)`', self.sql)
        if match:
            return match.group(1)
        else:
            raise ValueError("Table name not found in SQL file.")
        
    def check_table_exists(self, conn):
        """
        Check if the table already exists in the database.
        """
        query = f"SELECT COUNT(*) FROM information_schema.tables WHERE table_name = '{self.table_name}'"
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
        self.folder = os.path.join("build_DB", name)

    def build_db(self, conn_server):
        sql_path = os.path.join(self.folder, f"{self.name}_sql", "db.sql")
        build_obj = BuildDB(sql_path)
        build_obj.build(conn_server)
    
    def build_table(self, conn):
        for subclass in self.typeclass.__subclasses__():
            sql_path = os.path.join(self.folder, f"{self.name}_sql", f"{subclass.__name__}.sql")
            build_obj = subclass(sql_path)
            build_obj.build(conn)

               
    