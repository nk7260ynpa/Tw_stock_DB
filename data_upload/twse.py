from pydantic import BaseModel
from data_upload.base import DataUploadBase

from datetime import datetime

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
    def __init__(self, conn):
        self.conn = conn
        self.UploadType = UploadType

    def preprocess(self, df):
        df = df.drop(columns=['StockName'])
        return df
    


