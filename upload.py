import data_upload
from routers import MySQLRouter

import argparse

def main(opt):
    HOST = opt.host
    USER = opt.user
    PASSWORD = opt.password
    DBNAME = opt.dbname
    
    conn = MySQLRouter(HOST, USER, PASSWORD, DBNAME).mysql_conn
    package_name = DBNAME.lower()

    uploader = data_upload.__dict__[package_name].Uploader(conn)
    uploader.upload(opt.date)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload data to MySQL database.")
    parser.add_argument("--date", type=str, required=True, help="Date in YYYY-MM-DD format")
    parser.add_argument("--host", type=str, default="localhost:3306", help="MySQL host")
    parser.add_argument("--user", type=str, default="root", help="MySQL user")
    parser.add_argument("--password", type=str, default="stock", help="MySQL password")
    parser.add_argument("--dbname", type=str, default="TWSE", help="MySQL database name")
    opt = parser.parse_args()
    
    main(opt)