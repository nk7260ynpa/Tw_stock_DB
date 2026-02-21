import logging

import pandas as pd
from sqlalchemy import text

from build_DB.base import BaseBuild, BaseBuildTABLE

logger = logging.getLogger(__name__)

class BuildTWSE(BaseBuild):
    def __init__(self):
        super().__init__(BuildTWSETABLE, "TWSE")
    
class BuildTWSETABLE(BaseBuildTABLE):
    def __init__(self):
        super().__init__()
    
    def post_process(self):
        """
        No post-processing steps are defined in this class.
        """
        pass

class BuildTWSETABLEDailyPrice(BuildTWSETABLE):
    def __init__(self):
        super().__init__()
    
    def post_process(self, conn):
        pass

class BuildTWSETABLEStockName(BuildTWSETABLE):
    def __init__(self):
        super().__init__()

    def post_process(self, conn):
        """上傳證券代碼資料至 StockName 資料表。

        Args:
            conn: 資料庫連線物件。
        """
        df = pd.read_csv("build_DB/TWSE_sql/twse_code.csv", dtype=str)
        df.to_sql("StockName", conn, if_exists='append', index=False, chunksize=1000)
        conn.commit()

class BuildTWSETABLEIndustryMap(BuildTWSETABLE):
    def __init__(self):
        super().__init__()

    def post_process(self, conn):
        """上傳產業對照資料至 IndustryMap 資料表。

        Args:
            conn: 資料庫連線物件。
        """
        df = pd.read_csv("build_DB/TWSE_sql/twse_industry_map.csv", dtype=str)
        df.to_sql("IndustryMap", conn, if_exists='append', index=False, chunksize=1000)
        conn.commit()


class BuildTWSETABLECompanyInfo(BuildTWSETABLE):
    def __init__(self):
        super().__init__()

    def post_process(self, conn):
        """上傳公司資訊至 CompanyInfo 資料表。

        Args:
            conn: 資料庫連線物件。
        """
        df = pd.read_csv("build_DB/TWSE_sql/twse_company_info.csv", dtype=str)
        df.to_sql("CompanyInfo", conn, if_exists='append', index=False, chunksize=1000)
        conn.commit()

    def post_alter(self, conn, missing_columns):
        """新增欄位後，從 CSV 回填資料至既有資料列。

        Args:
            conn: 資料庫連線物件。
            missing_columns (set): 本次新增的欄位名稱集合。
        """
        df = pd.read_csv("build_DB/TWSE_sql/twse_company_info.csv", dtype=str)
        csv_columns = set(df.columns)
        update_cols = [c for c in missing_columns if c in csv_columns]
        if not update_cols:
            return

        update_df = df[df[update_cols[0]].notna() & (df[update_cols[0]] != '')]
        if update_df.empty:
            return

        set_clause = ', '.join(f'`{c}` = :{c}' for c in update_cols)
        sql = text(
            f"UPDATE `{self.table_name}` SET {set_clause} "
            f"WHERE `SecurityCode` = :SecurityCode"
        )

        params_list = []
        for _, row in update_df.iterrows():
            params = {'SecurityCode': row['SecurityCode']}
            for c in update_cols:
                val = row[c]
                params[c] = val if pd.notna(val) and val != '' else None
            params_list.append(params)

        for params in params_list:
            conn.execute(sql, params)
        conn.commit()
        logger.info(
            "資料表 '%s' 回填 %d 筆資料，欄位：%s",
            self.table_name, len(params_list), ', '.join(update_cols)
        )


class BuildTWSETABLETranslate(BuildTWSETABLE):
    def __init__(self):
        super().__init__()
    
    def post_process(self, conn):
        """
        Upload the translation column data match Translate table.
        
        Args:
            conn: Database connection object.
        """
        df = pd.read_csv("build_DB/TWSE_sql/twse_translate.csv")
        df.to_sql("Translate", conn, if_exists='append', index=False, chunksize=1000)
        conn.commit()

class BuildTWSETABLEUploadDate(BuildTWSETABLE):
    def __init__(self):
        super().__init__()
    
    def post_process(self, conn):
        pass
