import logging

from build_DB.base import BaseBuild, BaseBuildTABLE

logger = logging.getLogger(__name__)


class BuildSPECIAL_INFO(BaseBuild):
    """SPECIAL_INFO 資料庫建構類別。

    負責建立 SPECIAL_INFO 資料庫及其所有資料表。
    透過 BaseBuild 的 Factory pattern，自動發現並建構
    所有繼承自 BuildSPECIAL_INFOTABLE 的子類別。
    """

    def __init__(self):
        super().__init__(BuildSPECIAL_INFOTABLE, "SPECIAL_INFO")


class BuildSPECIAL_INFOTABLE(BaseBuildTABLE):
    """SPECIAL_INFO 資料表基類。

    所有 SPECIAL_INFO 資料庫的資料表建構類別皆繼承此類。
    類別命名規則：BuildSPECIAL_INFOTABLE{TableName}，
    對應 SQL 檔案路徑：build_DB/SPECIAL_INFO_sql/{TableName}.sql。
    """

    def __init__(self):
        super().__init__()

    def post_process(self):
        """建立資料表後的後處理步驟。

        此基類不定義任何後處理步驟，子類別可覆寫此方法。
        """
        pass


class BuildSPECIAL_INFOTABLEOilPrice(BuildSPECIAL_INFOTABLE):
    """OilPrice（國際原油價格）資料表建構類別。

    建立 SPECIAL_INFO.OilPrice 資料表，用於儲存國際原油價格資料。
    欄位包含日期、原油類型（WTI/Brent）、開盤價、最高價、最低價、
    收盤價與成交量。複合主鍵為 (Date, Product)。
    """

    def __init__(self):
        super().__init__()

    def post_process(self, conn):
        """建立資料表後的後處理步驟。

        OilPrice 資料表無需初始數據匯入，不執行任何後處理。

        Args:
            conn: 資料庫連線物件。
        """
        pass


class BuildSPECIAL_INFOTABLEOilPriceUploaded(BuildSPECIAL_INFOTABLE):
    """OilPriceUploaded（原油價格已上傳日期記錄）資料表建構類別。

    建立 SPECIAL_INFO.OilPriceUploaded 資料表，
    用於記錄已上傳原油價格資料的日期。
    """

    def __init__(self):
        super().__init__()

    def post_process(self, conn):
        """建立資料表後的後處理步驟。

        OilPriceUploaded 資料表無需初始數據匯入，不執行任何後處理。

        Args:
            conn: 資料庫連線物件。
        """
        pass
