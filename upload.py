import argparse
import logging

import data_upload
from routers import MySQLRouter

log_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
log_handler = logging.FileHandler("upload.log")
log_handler.setFormatter(log_formatter)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(log_handler)

def main(opt):
    """
    Main function to upload data to MySQL database.
    Args:
        opt (argparse.Namespace): Command line arguments 
        with the following attributes:
            - date (str): Date in YYYY-MM-DD format
            - host (str): MySQL host
            - user (str): MySQL user
            - password (str): MySQL password
            - dbname (str): MySQL database name
            - crawlerhost (str): Package name for data upload
    """
    HOST = opt.host
    USER = opt.user
    PASSWORD = opt.password
    DBNAME = opt.dbname
    CRAWLERHOST = opt.crawlerhost
    
    logger.info(f"Connecting to MySQL database {DBNAME} at {HOST} with user {USER}")
    conn = MySQLRouter(HOST, USER, PASSWORD, DBNAME).mysql_conn
    package_name = DBNAME.lower()

    logger.info(f"Uploading data for package: {package_name} on date: {opt.date}")
    uploader = data_upload.__dict__[package_name].Uploader(conn, CRAWLERHOST)
    uploader.upload(opt.date)
    conn.close()

    logger.info("All data uploaded successfully.")

    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload data to MySQL database.")
    parser.add_argument("--date", type=str, required=True, help="Date in YYYY-MM-DD format")
    parser.add_argument("--host", type=str, default="localhost:3306", help="MySQL host")
    parser.add_argument("--user", type=str, default="root", help="MySQL user")
    parser.add_argument("--password", type=str, default="stock", help="MySQL password")
    parser.add_argument("--dbname", type=str, choices=["TWSE", "TPEX"], default="TWSE", 
                        help="MySQL database name (choose between 'TWSE' and 'TPEX')")
    parser.add_argument("--crawlerhost", type=str, default="127.0.0.1:6738", 
                        help="Package name for data upload")
    opt = parser.parse_args()
    
    main(opt)