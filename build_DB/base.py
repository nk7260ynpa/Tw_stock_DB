import logging
import os
import re
from abc import ABC, abstractmethod

from sqlalchemy import text

logger = logging.getLogger(__name__)

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
            conn_server.commit()
            logger.info("資料庫 '%s' 建立成功", self.db_name)
        else:
            logger.info("資料庫 '%s' 已存在", self.db_name)


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
        query = text(f"""
                     SELECT COUNT(*) 
                     FROM information_schema.tables 
                     WHERE table_schema = DATABASE() AND table_name = '{self.table_name}'
                     """)
        result = conn.execute(query)
        count = result.fetchone()[0]
        return count > 0
    
    @abstractmethod
    def post_process(self):
        """
        Post-processing steps after the table is created.
        """
        pass

    def _get_defined_columns(self):
        """從 SQL 定義檔解析出所有欄位名稱與其定義。

        Returns:
            dict: 欄位名稱為 key，欄位定義（型別與約束）為 value。
                  例如 {'SecurityCode': 'VARCHAR(10) NOT NULL', ...}
        """
        columns = {}
        for line in self.sql.splitlines():
            line = line.strip()
            match = re.match(r'^`(\w+)`\s+(.+?)(?:,\s*)?$', line)
            if match:
                col_name = match.group(1)
                col_def = match.group(2).rstrip(',').strip()
                columns[col_name] = col_def
        return columns

    def _get_existing_columns(self, conn):
        """從 information_schema 查詢資料表現有的欄位名稱。

        Args:
            conn: 資料庫連線物件。

        Returns:
            set: 現有欄位名稱的集合。
        """
        query = text(
            f"SELECT COLUMN_NAME FROM information_schema.COLUMNS "
            f"WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = '{self.table_name}'"
        )
        result = conn.execute(query)
        return {row[0] for row in result.fetchall()}

    def _alter_table_add_columns(self, conn):
        """比對 SQL 定義與現有欄位，對缺少的欄位執行 ALTER TABLE ADD COLUMN。

        Args:
            conn: 資料庫連線物件。

        Returns:
            set: 本次新增的欄位名稱集合，若無缺少欄位則為空集合。
        """
        defined_columns = self._get_defined_columns()
        existing_columns = self._get_existing_columns(conn)
        missing_columns = set(defined_columns.keys()) - existing_columns

        for col_name in missing_columns:
            col_def = defined_columns[col_name]
            alter_sql = f"ALTER TABLE `{self.table_name}` ADD COLUMN `{col_name}` {col_def}"
            conn.execute(text(alter_sql))
            logger.info("資料表 '%s' 新增欄位 '%s'", self.table_name, col_name)

        if missing_columns:
            conn.commit()

        return missing_columns

    def post_alter(self, conn, missing_columns):
        """新增欄位後的資料回填處理。子類別可覆寫此方法。

        Args:
            conn: 資料庫連線物件。
            missing_columns (set): 本次新增的欄位名稱集合。
        """
        pass

    def build(self, conn):
        """建立資料表，或對既有資料表補上缺少的欄位並回填資料。

        Args:
            conn: 資料庫連線物件。
        """
        if not self.check_table_exists(conn):
            conn.execute(text(self.sql))
            conn.commit()
            self.post_process(conn)
            logger.info("資料表 '%s' 建立成功", self.table_name)
        else:
            missing_columns = self._alter_table_add_columns(conn)
            if missing_columns:
                self.post_alter(conn, missing_columns)
            logger.info("資料表 '%s' 已存在", self.table_name)

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
    