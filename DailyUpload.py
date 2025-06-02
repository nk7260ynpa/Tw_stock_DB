import upload
import datetime

from easydict import EasyDict 
import schedule
import time


def main():
    DATE = datetime.datetime.now().strftime("%Y-%m-%d")
    HOST = "localhost:3306"
    USER = "root"
    PASSWORD = "stock"
    DBNAME = "TWSE"
    opt = EasyDict({"date": DATE, 
                    "host": HOST, 
                    "user": USER, 
                    "password": PASSWORD, 
                    "dbname": DBNAME})
    upload.main(opt)


if __name__ == "__main__":
    # Schedule the task to run daily at 3:00 AM
    schedule.every().day.at("22:34").do(main)

    # Keep the script running to execute the scheduled task
    while True:
        schedule.run_pending()
        time.sleep(1)




