import logging

from pydantic import BaseModel
from datetime import datetime

from data_upload.base import DataUploadBase

logger = logging.getLogger(__name__)

class UploadType(BaseModel):
    Date: datetime
    SecurityCode: str
    MarginPurchase: int
    MarginSales: int
    CashRedemption: int
    MarginPurchaseBalanceOfPreviousDay: int
    MarginPurchaseBalanceOfTheDay: int
    MarginPurchaseQuotaForTheNextDay: int
    ShortCovering: int
    ShortSale: int
    StockRedemption: int
    ShortSaleBalanceOfPreviousDay: int
    ShortSaleBalanceOfTheDay: int
    ShortSaleQuotaForTheNextDay: int
    OffsettingOfMarginPurchasesAndShortSales: int
    Note: str

class Uploader(DataUploadBase):
    def __init__(self, conn, host):
        """
        Uploader class for uploading data to the MGTS database.
        
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
