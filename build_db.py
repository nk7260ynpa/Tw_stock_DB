from router import MySQLRouter
from sqlalchemy import text
import argparse

def main(args):
    databases = ["TWSE", "TPEX", "TAIFEX"]

    conn = MySQLRouter(args.host, args.user, args.password).mysql_conn
    for db_name in databases:
        create_db_query = f"CREATE DATABASE IF NOT EXISTS {db_name}"
        conn.execute(text(create_db_query))
        print(f"Database '{db_name}' created successfully.")
    print("All databases created successfully.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create MySQL databases.")
    parser.add_argument("--host", type=str, default="localhost:3306", help="MySQL host")
    parser.add_argument("--user", type=str, default="root", help="MySQL user")
    parser.add_argument("--password", type=str, default="stock", help="MySQL password")
    args = parser.parse_args()

    main(args)
    