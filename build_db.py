import mysql.connector

def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            password="stock",
            database="TWSE"
        )
        print("Connected to the database.")
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def execute_query(connection, query):
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        if query.strip().lower().startswith("select"):
            results = cursor.fetchall()
            for row in results:
                print(row)
        else:
            connection.commit()
            print("Query executed successfully.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()

if __name__ == "__main__":
    conn = connect_to_db()
    if conn:
        try:
            while True:
                sql_query = input("Enter SQL query (or type 'exit' to quit): ")
                if sql_query.lower() == "exit":
                    break
                execute_query(conn, sql_query)
        finally:
            conn.close()
            print("Connection closed.")