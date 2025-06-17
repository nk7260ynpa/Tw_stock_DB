import logging

from pydantic import BaseModel
from datetime import datetime

from data_upload.base import DataUploadBase

logger = logging.getLogger(__name__)

class UploadType(BaseModel):
    Date: datetime
    Contract: str
    ContractMonth: str
    Open: float
    High: float
    Low: float
    Last: float
    Change: float
    ChangePercent: float
    Volume: int
    SettlementPrice: float
    OpenInterest: float
    BestBid: float
    BestAsk: float
    HistoricalHigh: float
    HistoricalLow: float
    TradingHalt: float
    TradingSession: str
    SpreadOrderVolume: float
    
class Uploader(DataUploadBase):
    def __init__(self, conn, host):
        """
        Uploader class for uploading data to the TAIFEX database.
        
        Args:
            conn: Database connection object.
            host (str): Host address for the crawler service.
        """
        super().__init__(conn)
        self.UploadType = UploadType
        self.url = f"http://{host}"

    def preprocess(self, df):
        """
        No preprocessing steps are defined in this class.

        Args:
            df (pd.DataFrame): The DataFrame to preprocess.

        Returns:
            pd.DataFrame: The preprocessed DataFrame without the 'StockName' column.
        """
        return df
    