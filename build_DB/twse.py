import pandas as pd

from build_DB.base import BaseBuild, BaseBuildTABLE

class BuildTWSE(BaseBuild):
    def __init__(self):
        super().__init__(BuildTWSETABLE, "TWSE")
    
class BuildTWSETABLE(BaseBuildTABLE):
    def __init__(self):
        super().__init__()
    
    def post_process(self):
        """
        No post-processing steps are defined in this class.
        """
        pass

class BuildTWSETABLEDailyPrice(BuildTWSETABLE):
    def __init__(self):
        super().__init__()
    
    def post_process(self, conn):
        # Add any post-processing steps here
        pass

class BuildTWSETABLEStockName(BuildTWSETABLE):
    def __init__(self):
        super().__init__()
    
    def post_process(self, conn):
        df = pd.read_csv("build_DB/TWSE_sql/twse_code.csv")
        df.to_sql("StockName", conn, if_exists='append', index=False, chunksize=1000)
        conn.commit()

class BuildTWSETABLETranslate(BuildTWSETABLE):
    def __init__(self):
        super().__init__()
    
    def post_process(self, conn):
        # Add any post-processing steps here
        pass