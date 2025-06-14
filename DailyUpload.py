import time
import datetime

from easydict import EasyDict 
import schedule

import upload

def twse_daily_craw():
    """
    Daily Request Crawler and Upload Data to MySQL Database
    """
    DATE = datetime.datetime.now().strftime("%Y-%m-%d")
    HOST = "tw_stock_database:3306"
    USER = "root"
    PASSWORD = "stock"
    DBNAME = "TWSE"
    CRAWLERHOST = "tw_stocker_crawler:6738"
    opt = EasyDict({"host": HOST, 
                    "user": USER, 
                    "password": PASSWORD, 
                    "dbname": DBNAME, 
                    "crawlerhost": CRAWLERHOST})
    upload.day_upload("2024-06-14", opt)

def tpex_daily_craw():
    """
    Daily Request Crawler and Upload Data to MySQL Database
    """
    DATE = datetime.datetime.now().strftime("%Y-%m-%d")
    HOST = "tw_stock_database:3306"
    USER = "root"
    PASSWORD = "stock"
    DBNAME = "TPEX"
    CRAWLERHOST = "tw_stocker_crawler:6738"
    opt = EasyDict({"host": HOST, 
                    "user": USER, 
                    "password": PASSWORD, 
                    "dbname": DBNAME, 
                    "crawlerhost": CRAWLERHOST})
    upload.day_upload("2024-06-14", opt)


if __name__ == "__main__":
    schedule.every().day.at("18:40").do(twse_daily_craw)
    schedule.every().day.at("18:48").do(tpex_daily_craw)

    while True:
        schedule.run_pending()
        time.sleep(1)




