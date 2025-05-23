import build_DB

class BuildTWSETABLE(build_DB.BaseBuildTABLE):
    def __init__(self, sql_file_path):
        super().__init__(sql_file_path)
    
    def post_process(self):
        # Add any post-processing steps here
        pass

class BuildTWSETABLEDailyPrice(BuildTWSETABLE):
    def __init__(self, sql_file_path):
        super().__init__(sql_file_path)
    
    def post_process(self):
        # Add any post-processing steps here
        pass