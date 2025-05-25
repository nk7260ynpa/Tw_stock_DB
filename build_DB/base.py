import os
import re
from abc import ABC, abstractmethod

from sqlalchemy import text

class BuildEmptyDB():    
    def __init__(self, sql_file_path):
        """
        sql_file_path (str): The path to the SQL file that contains the command to create the database.
        """
        self.sql_file_path = sql_file_path
        self.sql = self.read_sql_file()
        self.db_name = self.get_db_name()

    def read_sql_file(self):
        """
        Read the SQL file to get the SQL command for creating the database.

        Args:
            self.sql_file_path (str): The path to the SQL file.

        Returns:
            str: The SQL command as a string.
        """
        with open(self.sql_file_path, 'r') as file:
            sql = file.read()
        return sql

    def get_db_name(self):
        """
        According to the SQL command, extract the database name from the SQL string.
        
        Returns:
            str: The name of the database.
        """
        start = self.sql.find("`") + 1
        end = self.sql.find("`", start)
        return self.sql[start:end]
    
    def check_db_exists(self, conn):
        """
        Check if the database already exists.
        
        Args:
            conn: The database connection object.

        Returns:
            bool: True if the database exists, False otherwise.
        """
        query = text(f"SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = '{self.db_name}'")
        results = conn.execute(query)
        rows = results.fetchall()
        if len(rows) > 0:
            return True
        else:
            return False
        
    def build(self, conn_server):
        """
        Build the database using the SQL command read from the file.
        
        Args:
            conn_server: The database connection object to execute the SQL command.
        
        Returns:
            None
        """
        if not self.check_db_exists(conn_server):
            conn_server.execute(text(self.sql))
            print(f"Database '{self.db_name}' created successfully.")
        else:
            print(f"Database '{self.db_name}' already exists.")
        conn_server.close()


class BaseBuildTABLE(ABC):
    def __init__(self):
        """
        According to the class name, extract the folder name and table name.
        """
        folder_name = re.search(r'Build(.*?)TABLE', self.__class__.__name__).group(1)
        table_name = re.search(r'TABLE(.*)', self.__class__.__name__).group(1)  
        self.sql_file_path = os.path.join("build_DB", folder_name+"_sql", f"{table_name}.sql")
        self.sql = self.read_sql_file()
        self.table_name = table_name
        
    def read_sql_file(self):
        """
        Read the SQL file to get the SQL command for creating the table.
        Args:
            self.sql_file_path (str): The path to the SQL file.
        Returns:
            str: The SQL command as a string.
        """

        with open(self.sql_file_path, 'r') as file:
            sql = file.read()
        return sql
        
    def check_table_exists(self, conn):
        """
        Check if the table already exists in the database.

        Args:
            conn: The database connection object.
        """
        query = text(f"SELECT COUNT(*) FROM information_schema.tables WHERE table_name = '{self.table_name}'")
        result = conn.execute(query)
        count = result.fetchone()[0]
        return count > 0
    
    @abstractmethod
    def post_process(self):
        """
        Post-processing steps after the table is created.
        """
        pass
    
    def build(self, conn):
        """
        Build the table using the SQL command read from the file.
        
        Args:
            conn: The database connection object to execute the SQL command.
        """
        if not self.check_table_exists(conn):
            conn.execute(text(self.sql))
            conn.commit()
            self.post_process(conn)
            print(f"Table '{self.table_name}' created successfully.")
        else:
            print(f"Table '{self.table_name}' already exists.")

class BaseBuild(ABC):
    def __init__(self, typeclass, name):
        """
        Initialize the BaseBuild class with a typeclass and name.
        Args:
            typeclass (type): The class type that will be used to build the database.
            name (str): The name of the database.
        """ 
        self.typeclass = typeclass
        self.name = name
        self.folder = os.path.join("build_DB")

    def build_db(self, conn_server):
        """
        Build the database using the SQL file associated with the typeclass.

        Args:
            conn_server: The database connection object to execute the SQL command.
        """
        sql_path = os.path.join(self.folder, f"{self.name}_sql", "db.sql")
        build_obj = BuildEmptyDB(sql_path)
        build_obj.build(conn_server)
    
    def build_table(self, conn):
        """
        Build the tables in the database using the SQL files associated with the subclasses of the typeclass.
        
        Args:
            conn: The database connection object to execute the SQL commands.
        """
        for subclass in self.typeclass.__subclasses__():
            build_obj = subclass()
            build_obj.build(conn)
    