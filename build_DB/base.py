from abc import ABC, abstractmethod
import re
from sqlalchemy import text

class BaseBuildTABLE(ABC):
    def __init__(self, sql_file_path):
        self.sql_file_path = sql_file_path
        self.sql = self.read_sql_file()
        self.table_name = self.get_table_name()
        
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
    
    def build(self, conn):
        if not self.check_table_exists(conn):
            conn.execute(text(self.sql))
            print(f"Table '{self.table_name}' created successfully.")
        else:
            print(f"Table '{self.table_name}' already exists.")

    @abstractmethod
    def post_process(self, conn):
        pass