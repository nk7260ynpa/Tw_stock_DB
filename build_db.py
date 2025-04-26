from mysql.connector import Error

import mysql.connector

def create_stock_database():
    try:
        # Connect to MySQL server
        connection = mysql.connector.connect(
            host='localhost',
            port=3306,
            user='root',  # Replace with your MySQL username
            password='stock'  # Replace with your MySQL password
        )

        if connection.is_connected():
            print("Connected to MySQL server.")
            cursor = connection.cursor()

            # Prompt user for database name
            db_name = input("Enter the name of the database to create: ")
            create_db_query = f"CREATE DATABASE {db_name}"
            
            # Execute the query
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
    create_database()