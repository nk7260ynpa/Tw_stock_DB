from build_DB.base import BaseBuild, BaseBuildTABLE

class BuildTWSE(BaseBuild):
    def __init__(self):
        super().__init__(BuildTWSETABLE, "TWSE")
    
class BuildTWSETABLE(BaseBuildTABLE):
    def __init__(self):
        super().__init__()
    
    def post_process(self):
        # Add any post-processing steps here
        pass

class BuildTWSETABLEDailyPrice(BuildTWSETABLE):
    def __init__(self):
        super().__init__()
    
    def post_process(self):
        # Add any post-processing steps here
        pass
