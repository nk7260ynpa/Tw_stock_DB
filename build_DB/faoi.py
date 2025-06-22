import pandas as pd

from build_DB.base import BaseBuild, BaseBuildTABLE

class BuildFAOI(BaseBuild):
    def __init__(self):
        super().__init__(BuildFAOITABLE, "FAOI")
    
class BuildFAOITABLE(BaseBuildTABLE):
    def __init__(self):
        super().__init__()
    
    def post_process(self):
        """
        No post-processing steps are defined in this class.
        """
        pass

class BuildFAOITABLEDailyPrice(BuildFAOITABLE):
    def __init__(self):
        super().__init__()
    
    def post_process(self, conn):
        pass

class BuildFAOITABLEStockName(BuildFAOITABLE):
    def __init__(self):
        super().__init__()
    
    def post_process(self, conn):
        """
        Upload the Security Code data match StockName table.

        Args:
            conn: Database connection object.
        """
        df = pd.read_csv("build_DB/FAOI_sql/faoi_code.csv")
        df.to_sql("StockName", conn, if_exists='append', index=False, chunksize=1000)
        conn.commit()

class BuildFAOITABLETranslate(BuildFAOITABLE):
    def __init__(self):
        super().__init__()
    
    def post_process(self, conn):
        """
        Upload the translation column data match Translate table.
        
        Args:
            conn: Database connection object.
        """
        df = pd.read_csv("build_DB/FAOI_sql/faoi_translate.csv")
        df.to_sql("Translate", conn, if_exists='append', index=False, chunksize=1000)
        conn.commit()

class BuildFAOITABLEUploadDate(BuildFAOITABLE):
    def __init__(self):
        super().__init__()
    
    def post_process(self, conn):
        pass
