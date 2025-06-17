import pandas as pd

from build_DB.base import BaseBuild, BaseBuildTABLE

class BuildTAIFEX(BaseBuild):
    def __init__(self):
        super().__init__(BuildTAIFEXTABLE, "TAIFEX")

class BuildTAIFEXTABLE(BaseBuildTABLE):
    def __init__(self):
        super().__init__()

    def post_process(self):
        """
        No post-processing steps are defined in this class.
        """
        pass

class BuildTAIFEXTABLEDailyPrice(BuildTAIFEXTABLE):
    def __init__(self):
        super().__init__()
    
    def post_process(self, conn):
        # Add any post-processing steps here
        pass

class BuildTAIFEXTABLETranslate(BuildTAIFEXTABLE):
    def __init__(self):
        super().__init__()
    
    def post_process(self, conn):
        """
        Upload the translation column data match Translate table.
        
        Args:
            conn: Database connection object.
        """
        df = pd.read_csv("build_DB/TAIFEX_sql/TAIFEX_translate.csv")
        df.to_sql("Translate", conn, if_exists='append', index=False, chunksize=1000)
        conn.commit()

class BuildTAIFEXTABLEUploadDate(BuildTAIFEXTABLE):
    def __init__(self):
        super().__init__()
    
    def post_process(self, conn):
        pass