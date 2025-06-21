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
