from pydantic import BaseModel
from data_upload.base import DataUploadBase

from datetime import datetime

import tw_crawler

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
        self.crawler = tw_crawler.twse_crawler

    def preprocess(self, df):
        df = df.drop(columns=['StockName'])
        return df
    


