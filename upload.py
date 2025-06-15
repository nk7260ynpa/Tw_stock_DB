import argparse
import logging

from datetime import datetime, timedelta

import data_upload
from routers import MySQLRouter
import random
import time

log_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
log_handler = logging.FileHandler("upload.log")
log_handler.setFormatter(log_formatter)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(log_handler)

def day_upload(date, opt):
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

    logger.info(f"Uploading data for package: {package_name} on date: {date}")
    uploader = data_upload.__dict__[package_name].Uploader(conn, CRAWLERHOST)
    uploader.upload(date)
    conn.close()

    logger.info("All data uploaded successfully.")

def main(opt):
    """
    Main function to handle command line arguments and call the upload function.
    Args:
        opt (argparse.Namespace): Command line arguments
    """
    if not opt.end_date:
        opt.end_date = opt.start_date

    start_date = opt.start_date
    end_date = opt.end_date

    logger.info(f"Starting upload from {start_date} to {end_date}")
    
    start_dt = datetime.strptime(start_date, "%Y-%m-%d")
    end_dt = datetime.strptime(end_date, "%Y-%m-%d")

    # Loop through each date in the range
    current_dt = start_dt
    while current_dt <= end_dt:
        # Randomly pause for 3 to 15 seconds
        pause_duration = random.uniform(3, 15)
        logger.info(f"Pausing for {pause_duration} seconds before processing date: {current_dt.strftime('%Y-%m-%d')}")
        time.sleep(pause_duration)
        date_str = current_dt.strftime("%Y-%m-%d")
        day_upload(date_str, opt)
        current_dt += timedelta(days=1)

    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload data to MySQL database.")
    parser.add_argument("--start_date", type=str, required=True, help="Date in YYYY-MM-DD format")
    parser.add_argument("--end_date", type=str, default="", help="Date in YYYY-MM-DD format")
    parser.add_argument("--host", type=str, default="localhost:3306", help="MySQL host")
    parser.add_argument("--user", type=str, default="root", help="MySQL user")
    parser.add_argument("--password", type=str, default="stock", help="MySQL password")
    parser.add_argument("--dbname", type=str, choices=["TWSE", "TPEX", "TAIFEX"], default="TWSE", 
                        help="MySQL database name (choose between 'TWSE' and 'TPEX' and 'TAIFEX')")
    parser.add_argument("--crawlerhost", type=str, default="127.0.0.1:6738", 
                        help="Package name for data upload")
    opt = parser.parse_args()
    
    main(opt)