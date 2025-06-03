import time
import datetime

from easydict import EasyDict 
import schedule

import upload

def main():
    """
    Daily Request Crawler and Upload Data to MySQL Database
    """
    DATE = datetime.datetime.now().strftime("%Y-%m-%d")
    HOST = "tw_stock_database:3306"
    USER = "root"
    PASSWORD = "stock"
    DBNAME = "TWSE"
    CRAWLERHOST = "tw_stocker_crawler:6738"
    opt = EasyDict({"date": DATE, 
                    "host": HOST, 
                    "user": USER, 
                    "password": PASSWORD, 
                    "dbname": DBNAME, 
                    "crawlerhost": CRAWLERHOST})
    upload.main(opt)


if __name__ == "__main__":
    schedule.every().day.at("16:13").do(main)

    while True:
        schedule.run_pending()
        time.sleep(1)




