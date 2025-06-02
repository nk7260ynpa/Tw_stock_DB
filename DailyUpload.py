import upload
import datetime

from easydict import EasyDict 
import schedule
import time


def main():
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
    # Schedule the task to run daily at 3:00 AM
    schedule.every().day.at("16:31").do(main)

    # Keep the script running to execute the scheduled task
    while True:
        schedule.run_pending()
        time.sleep(1)




