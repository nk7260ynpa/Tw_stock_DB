import upload
import datetime

from easydict import EasyDict 

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
    main()


