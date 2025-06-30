import pandas as pd

from build_DB.base import BaseBuild, BaseBuildTABLE

class BuildTWSE(BaseBuild):
    def __init__(self):
        super().__init__(BuildMGSTTABLE, "TWSE")
    
class BuildMGSTTABLE(BaseBuildTABLE):
    def __init__(self):
        super().__init__()
    
    def post_process(self):
        """
        No post-processing steps are defined in this class.
        """
        pass
