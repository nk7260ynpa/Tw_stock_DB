import time
import random
import datetime

from easydict import EasyDict 
import schedule

import upload

def daily_craw(db_name):
    """
    Daily Request Crawler and Upload Data to MySQL Database
    
    Args:
        db_name (str): Name of the database to upload data to. 
                       Options are "TWSE", "TPEX", or "TAIFEX".
    """
    HOST = "tw_stock_database:3306"
    USER = "root"
    PASSWORD = "stock"
    DBNAME = db_name
    CRAWLERHOST = "tw_stocker_crawler:6738"
    opt = EasyDict({"host": HOST, 
                    "user": USER, 
                    "password": PASSWORD, 
                    "dbname": DBNAME, 
                    "crawlerhost": CRAWLERHOST})
    
    date_list = [(datetime.datetime.now() - datetime.timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]
    for date in date_list:
        pause_duration = random.uniform(3, 15)
        time.sleep(pause_duration)
        upload.day_upload(date, opt)

if __name__ == "__main__":
    schedule.every().day.at("16:10").do(daily_craw, "TWSE")
    schedule.every().day.at("16:18").do(daily_craw, "TPEX")
    schedule.every().day.at("16:23").do(daily_craw, "TAIFEX")

    while True:
        schedule.run_pending()
        time.sleep(1)




