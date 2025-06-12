import os
import requests
from abc import ABC, abstractmethod

import pandas as pd
from sqlalchemy import text

import logging
logger = logging.getLogger(__name__)

class DataUploadBase(ABC):
    @abstractmethod
    def __init__(self, conn):
        """
        Initialize the DataUploadBase class with a database connection.

        Args:
            conn: Database connection object.

        Returns:
            self.name: The name of the data type
            self.conn: The database connection object.
        """
        self.name = os.path.basename(type(self).__module__.split('.')[-1])
        self.conn = conn

    @abstractmethod
    def preprocess(self, df):
        """
        Preprocess the DataFrame before uploading to the database. 
        """
        pass

    def craw_data(self, date):
        """
        According to the date, crawl the data from the crawler service.
        
        Args:
            date (str): Date in YYYY-MM-DD format.
        
        Returns:
            pd.DataFrame: DataFrame containing daily price data.
        """
        payload = {"name": self.name, "date": date}
        response = requests.post(self.url, params=payload)
        json_data = response.json()["data"]
        df = pd.read_json(json_data, orient="records")
        return df
    
    def check_schema(self, df):
        """
        Check the schema of the DataFrame to ensure it matches the UploadType model.
        
        Args:
            df (pd.DataFrame): The DataFrame to check.
        
        Returns:
            pd.DataFrame: The DataFrame with the schema checked and converted to the UploadType model.
        """
        df_dict = df.to_dict(orient='records')
        df_schema = [self.UploadType(**record).__dict__ for record in df_dict]
        df = pd.DataFrame(df_schema)
        return df
    
    def check_date(self, date):
        """
        Check if the date already exists in the UploadDate table.

        Args:
            date (str): Date in YYYY-MM-DD format.
        """
        if self.conn.execute(text(f"SELECT COUNT(*) FROM UploadDate WHERE Date = '{date}'")).scalar():
            return True
        return False
            
    def upload_df(self, df):
        """
        Upload the Daily Data to the DailyPrice table in the database.
        
        Args:
            df (pd.DataFrame): The DataFrame containing daily price data.
        """
        df_copy = self.preprocess(df.copy())
        df_copy = self.check_schema(df_copy)
        df_copy.to_sql("DailyPrice", self.conn, if_exists='append', index=False, chunksize=1000)
        self.conn.commit()

    def upload_date(self, date):
        """
        Upload the date to the UploadDate table.
        
        Args:
            date (str): Date in YYYY-MM-DD format.
        """
        update = text(f"INSERT INTO UploadDate (Date) VALUES ('{date}');")
        self.conn.execute(update)
        self.conn.commit()

    def upload(self, date):
        """
        If data for the date already exists, it skips the upload.
        Otherwise, it crawls the data and uploads it to the database.

        Args:
            date (str): Date in YYYY-MM-DD format.
        """
        if self.check_date(date):
           logger.info(f"Data for {date} already exists in the database. Skipping upload.")
           pass
        else:
           df = self.craw_data(date)
           self.upload_df(df)
           self.upload_date(date)
        logger.info(f"Data for {date} uploaded successfully to the database.")
