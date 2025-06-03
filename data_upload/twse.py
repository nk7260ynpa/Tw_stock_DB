from pydantic import BaseModel
from datetime import datetime

from data_upload.base import DataUploadBase


import logging
logger = logging.getLogger(__name__)

class UploadType(BaseModel):
    Date: datetime
    SecurityCode: str
    TradeVolume: int
    Transaction: int
    TradeValue: int
    OpeningPrice: float
    HighestPrice: float
    LowestPrice: float
    ClosingPrice: float
    Change: float
    LastBestBidPrice: float
    LastBestBidVolume: int
    LastBestAskPrice: float
    LastBestAskVolume: int
    PriceEarningratio: float


class Uploader(DataUploadBase):
    def __init__(self, conn, host):
        """
        Uploader class for uploading data to the TWSE database.
        
        Args:
            conn: Database connection object.
            host (str): Host address for the crawler service.
        """
        super().__init__(conn)
        self.UploadType = UploadType
        self.url = f"http://{host}"

    def preprocess(self, df):
        """
        Preprocess the DataFrame by dropping the 'StockName' column.
        for upload to DailyPrice table.
        Args:
            df (pd.DataFrame): The DataFrame to preprocess.

        Returns:
            pd.DataFrame: The preprocessed DataFrame without the 'StockName' column.
        """
        df = df.drop(columns=['StockName'])
        return df
    