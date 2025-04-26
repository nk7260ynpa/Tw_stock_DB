import mysql.connector

# Database connection configuration
config = {
    'user': 'root',  # Replace with your MySQL username
    'password': 'stock',  # Replace with your MySQL password
    'host': '127.0.0.1',
    'port': 3306,
    'database': 'TWSE'  # Replace with your database name
}

try:
    # Connect to the database
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    # Read the SQL file
    with open('tpex.sql', 'r') as file:
        sql_commands = file.read()

    # Execute the SQL commands
    for command in sql_commands.split(';'):
        if command.strip():  # Skip empty commands
            cursor.execute(command)
            print(f"Executed: {command.strip()}")

    # Commit changes
    connection.commit()

except mysql.connector.Error as err:
    print(f"Error: {err}")
finally:
    # Close the connection
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("Database connection closed.")