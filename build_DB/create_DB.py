from sqlalchemy import text

class BuildDB():    
    def __init__(self, sql_file_path):
        self.sql_file_path = sql_file_path
        self.sql = self.read_sql_file()
        self.db_name = self.get_db_name()

    def read_sql_file(self):
        with open(self.sql_file, 'r') as file:
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
        
    def build(self, conn):
        if not self.check_db_exists(conn):
            conn.execute(text(self.sql))
            print(f"Database '{self.db_name}' created successfully.")
        else:
            print(f"Database '{self.db_name}' already exists.")
        conn.close()

