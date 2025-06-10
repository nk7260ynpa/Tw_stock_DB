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

