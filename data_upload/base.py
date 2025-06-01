from abc import ABC, abstractmethod
import os
import requests

import pandas as pd
from sqlalchemy import text

class DataUploadBase(ABC):
    @abstractmethod
    def __init__(self, conn):
        self.url = "http://127.0.0.1:6738"
        self.name = os.path.basename(type(self).__module__.split('.')[-1])
        self.conn = conn

    @abstractmethod
    def preprocess(self, df):
        pass

    def craw_data(self, date):
        payload = {"name": self.name, "date": date}
        response = requests.post(self.url, params=payload)
        json_data = response.json()["data"]
        df = pd.read_json(json_data, orient="records")
        return df
    
    def check_schema(self, df):
        df_dict = df.to_dict(orient='records')
        df_schema = [self.UploadType(**record).__dict__ for record in df_dict]
        df = pd.DataFrame(df_schema)
        return df
    
    def check_date(self, date):
        if self.conn.execute(text(f"SELECT COUNT(*) FROM UploadDate WHERE Date = {date}")).scalar():
            return True
        return False
            
    def upload_df(self, df):
        df_copy = self.preprocess(df.copy())
        df_copy = self.check_schema(df_copy)
        df_copy.to_sql("DailyPrice", self.conn, if_exists='append', index=False, chunksize=1000)
        self.conn.commit()

    def upload_date(self, date):
        update = text(f"INSERT INTO UploadDate (Date) VALUES ('{date}');")
        self.conn.execute(update)
        self.conn.commit()

    def upload(self, date):
        df = self.craw_data(date)

        if self.check_date(date):
           pass
        else:
           self.upload_df(df)
           self.upload_date(date)
