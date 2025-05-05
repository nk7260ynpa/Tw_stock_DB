from mysql.connector import Error
from conncli import connect_server
import mysql.connector

def create_stock_database():
    try:
        # Connect to MySQL server
        connection = connect_server("localhost", "root", "stock")  # Replace with your credentials
        if connection.is_connected():
            print("Connected to MySQL server.")
            cursor = connection.cursor()

            # Create databases for TWSE, TPEX, and TAIFEX
            databases = ["TWSE", "TPEX", "TAIFEX"]
            for db_name in databases:
                create_db_query = f"CREATE DATABASE IF NOT EXISTS {db_name}"
                cursor.execute(create_db_query)
                print(f"Database '{db_name}' created successfully.")

    except Error as e:
        print(f"Error: {e}")
        
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed.")

if __name__ == "__main__":
    create_stock_database()