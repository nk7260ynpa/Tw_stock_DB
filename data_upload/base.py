from abc import ABC, abstractmethod

import pandas as pd
from sqlalchemy import text

class DataUploadBase(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def preprocess(self, df):
        pass
    
    def check_schema(self, df):
        df_dict = df.to_dict(orient='records')
        df_schema = [self.UploadType(**record).__dict__ for record in df_dict]
        df = pd.DataFrame(df_schema)
        return df

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
        df = self.crawler(date)
        self.upload_df(df)
        self.upload_date(date)
