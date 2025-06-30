import pandas as pd

from build_DB.base import BaseBuild, BaseBuildTABLE

class BuildMGTS(BaseBuild):
    def __init__(self):
        super().__init__(BuildMGTSTABLE, "MGTS")
    
class BuildMGTSTABLE(BaseBuildTABLE):
    def __init__(self):
        super().__init__()
    
    def post_process(self):
        """
        No post-processing steps are defined in this class.
        """
        pass

class BuildMGTSTABLEDailyPrice(BuildMGTSTABLE):
    def __init__(self):
        super().__init__()
    
    def post_process(self, conn):
        pass

class BuildMGTSTABLEStockName(BuildMGTSTABLE):
    def __init__(self):
        super().__init__()
    
    def post_process(self, conn):
        """
        Upload the Security Code data match StockName table.

        Args:
            conn: Database connection object.
        """
        df = pd.read_csv("build_DB/MGTS_sql/mgts_code.csv")
        df.to_sql("StockName", conn, if_exists='append', index=False, chunksize=1000)
        conn.commit()
