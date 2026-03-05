import logging

import pandas as pd

from build_DB.base import BaseBuild, BaseBuildTABLE

logger = logging.getLogger(__name__)


class BuildINFO(BaseBuild):
    """INFO 資料庫建構類別。

    負責建立 INFO 資料庫及其所有資料表。
    透過 BaseBuild 的 Factory pattern，自動發現並建構
    所有繼承自 BuildINFOTABLE 的子類別。
    """

    def __init__(self):
        super().__init__(BuildINFOTABLE, "INFO")


class BuildINFOTABLE(BaseBuildTABLE):
    """INFO 資料表基類。

    所有 INFO 資料庫的資料表建構類別皆繼承此類。
    類別命名規則：BuildINFOTABLE{TableName}，
    對應 SQL 檔案路徑：build_DB/INFO_sql/{TableName}.sql。
    """

    def __init__(self):
        super().__init__()

    def post_process(self):
        """建立資料表後的後處理步驟。

        此基類不定義任何後處理步驟，子類別可覆寫此方法。
        """
        pass


class BuildINFOTABLEKnowledge(BuildINFOTABLE):
    """Knowledge（台股知識庫）資料表建構類別。

    建立 INFO.Knowledge 資料表，用於儲存台股相關知識。
    欄位包含 id（自動遞增主鍵）、category（分類）、term（名詞）與
    description（說明）。建立後自動從 CSV 匯入初始知識資料。
    """

    def __init__(self):
        super().__init__()

    def post_process(self, conn):
        """建立資料表後匯入初始知識資料。

        從 build_DB/INFO_sql/knowledge_data.csv 讀取知識資料，
        並以 pandas 寫入 Knowledge 資料表。

        Args:
            conn: 資料庫連線物件。
        """
        df = pd.read_csv("build_DB/INFO_sql/knowledge_data.csv")
        df.to_sql(
            "Knowledge", conn,
            if_exists='append', index=False, chunksize=1000
        )
        conn.commit()
        logger.info("已匯入 %d 筆知識資料至 Knowledge 資料表", len(df))
