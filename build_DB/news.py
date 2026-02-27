import logging

from build_DB.base import BaseBuild, BaseBuildTABLE

logger = logging.getLogger(__name__)


class BuildNEWS(BaseBuild):
    """NEWS 資料庫建構類別。

    負責建立 NEWS 資料庫及其所有資料表。
    透過 BaseBuild 的 Factory pattern，自動發現並建構
    所有繼承自 BuildNEWSTABLE 的子類別。
    """

    def __init__(self):
        super().__init__(BuildNEWSTABLE, "NEWS")


class BuildNEWSTABLE(BaseBuildTABLE):
    """NEWS 資料表基類。

    所有 NEWS 資料庫的資料表建構類別皆繼承此類。
    類別命名規則：BuildNEWSTABLE{TableName}，
    對應 SQL 檔案路徑：build_DB/NEWS_sql/{TableName}.sql。
    """

    def __init__(self):
        super().__init__()

    def post_process(self):
        """建立資料表後的後處理步驟。

        此基類不定義任何後處理步驟，子類別可覆寫此方法。
        """
        pass


class BuildNEWSTABLECTEE(BuildNEWSTABLE):
    """CTEE（工商時報）新聞資料表建構類別。

    建立 NEWS.CTEE 資料表，用於儲存工商時報的新聞資料。
    欄位包含日期、時間、作者、標題、副標題、標籤與網址。
    """

    def __init__(self):
        super().__init__()

    def post_process(self, conn):
        """建立資料表後的後處理步驟。

        CTEE 資料表無需初始數據匯入，不執行任何後處理。

        Args:
            conn: 資料庫連線物件。
        """
        pass


class BuildNEWSTABLECTEEUploaded(BuildNEWSTABLE):
    """CTEEUploaded 資料表建構類別。

    建立 NEWS.CTEEUploaded 資料表，用於記錄已抓取過 CTEE 新聞的日期。
    """

    def __init__(self):
        super().__init__()

    def post_process(self, conn):
        """建立資料表後的後處理步驟。

        CTEEUploaded 資料表無需初始數據匯入，不執行任何後處理。

        Args:
            conn: 資料庫連線物件。
        """
        pass
