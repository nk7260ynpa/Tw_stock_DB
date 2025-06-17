import pandas as pd

from build_DB.base import BaseBuild, BaseBuildTABLE

class BuildTPEX(BaseBuild):
    def __init__(self):
        super().__init__(BuildTPEXTABLE, "TPEX")

class BuildTPEXTABLE(BaseBuildTABLE):
    def __init__(self):
        super().__init__()

    def post_process(self):
        """
        No post-processing steps are defined in this class.
        """
        pass

class BuildTPEXTABLEDailyPrice(BuildTPEXTABLE):
    def __init__(self):
        super().__init__()
    
    def post_process(self, conn):
        pass

class BuildTPEXTABLEStockName(BuildTPEXTABLE):
    def __init__(self):
        super().__init__()
    
    def post_process(self, conn):
        """
        Upload the Code data match Name table.

        Args:
            conn: Database connection object.
        """
        df = pd.read_csv("build_DB/TPEX_sql/tpex_code.csv")
        df.to_sql("StockName", conn, if_exists='append', index=False, chunksize=1000)
        conn.commit()

class BuildTPEXTABLETranslate(BuildTPEXTABLE):
    def __init__(self):
        super().__init__()
    
    def post_process(self, conn):
        """
        Upload the translation column data match Translate table.
        
        Args:
            conn: Database connection object.
        """
        df = pd.read_csv("build_DB/TPEX_sql/tpex_translate.csv")
        df.to_sql("Translate", conn, if_exists='append', index=False, chunksize=1000)
        conn.commit()

class BuildTPEXTABLEUploadDate(BuildTPEXTABLE):
    def __init__(self):
        super().__init__()
    
    def post_process(self, conn):
        pass
