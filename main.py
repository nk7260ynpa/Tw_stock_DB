import argparse

import build_DB
from routers import MySQLRouter

def main(opt):
    """
    Main function to build the database and tables.
    Args:
        opt (argparse.Namespace): Command line arguments 
        with the following attributes:
            - host (str): MySQL host
            - user (str): MySQL user
            - password (str): MySQL password
    """
    HOST = opt.host
    USER = opt.user
    PASSWORD = opt.password
    
    all_subclasses = build_DB.BaseBuild.__subclasses__()
    conn_server = MySQLRouter(HOST, USER, PASSWORD).mysql_conn

    for subclass in all_subclasses:
        build_DB_obj = subclass()
        build_DB_obj.build_db(conn_server)
        conn_db = MySQLRouter(HOST, USER, PASSWORD, build_DB_obj.name).mysql_conn
        build_DB_obj.build_table(conn_db)
        conn_db.close()
    
    conn_server.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build the database and tables.")
    parser.add_argument("--host", type=str, default="localhost:3306", help="Database host")
    parser.add_argument("--user", type=str, default="root", help="Database user")
    parser.add_argument("--password", type=str, default="stock", help="Database password")
    opt = parser.parse_args()
    main(opt)
    