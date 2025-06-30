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
