import argparse
import logging

from sqlalchemy import text

import build_DB
from routers import MySQLRouter

logger = logging.getLogger(__name__)

MGTS_MIGRATION_MAP = {
    "DailyPrice": "MGTSDailyPrice",
    "Translate": "Translate",
    "UploadDate": "MGTSUploadDate",
}


def consolidate_mgts_tables(conn_server):
    """合併 TWSE 中的 MGTS 冗餘資料表。

    處理既有資料庫的遷移：
    1. 加寬 Translate 的 English 欄位至 VARCHAR(45)
    2. 將 MGTSTranslate 的資料合併至 Translate
    3. 刪除 MGTSStockName 和 MGTSTranslate 資料表

    Args:
        conn_server: 資料庫連線物件（不指定資料庫）。
    """
    result = conn_server.execute(
        text("SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA "
             "WHERE SCHEMA_NAME = 'TWSE'")
    )
    if not result.fetchone():
        logger.info("TWSE 資料庫不存在，跳過合併")
        return

    col_info = conn_server.execute(
        text("SELECT CHARACTER_MAXIMUM_LENGTH FROM INFORMATION_SCHEMA.COLUMNS "
             "WHERE TABLE_SCHEMA = 'TWSE' AND TABLE_NAME = 'Translate' "
             "AND COLUMN_NAME = 'English'")
    )
    col_row = col_info.fetchone()
    if col_row and col_row[0] < 45:
        conn_server.execute(
            text("ALTER TABLE `TWSE`.`Translate` "
                 "MODIFY COLUMN `English` VARCHAR(45) NOT NULL")
        )
        conn_server.commit()
        logger.info("已加寬 TWSE.Translate.English 欄位至 VARCHAR(45)")

    mgts_translate_exists = conn_server.execute(
        text("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES "
             "WHERE TABLE_SCHEMA = 'TWSE' AND TABLE_NAME = 'MGTSTranslate'")
    ).fetchone()
    if mgts_translate_exists:
        conn_server.execute(
            text("INSERT IGNORE INTO `TWSE`.`Translate` "
                 "SELECT * FROM `TWSE`.`MGTSTranslate`")
        )
        conn_server.commit()
        logger.info("已將 TWSE.MGTSTranslate 資料合併至 TWSE.Translate")

    for table in ("MGTSStockName", "MGTSTranslate"):
        table_exists = conn_server.execute(
            text("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES "
                 "WHERE TABLE_SCHEMA = 'TWSE' AND TABLE_NAME = :tbl"),
            {"tbl": table}
        ).fetchone()
        if table_exists:
            conn_server.execute(
                text(f"DROP TABLE `TWSE`.`{table}`")
            )
            conn_server.commit()
            logger.info("已刪除 TWSE.%s 資料表", table)


def migrate_mgts_to_twse(conn_server):
    """將舊 MGTS 資料庫的資料搬移至 TWSE 的 MGTS 前綴資料表，並刪除舊資料庫。

    Args:
        conn_server: 資料庫連線物件（不指定資料庫）。
    """
    result = conn_server.execute(
        text("SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA "
             "WHERE SCHEMA_NAME = 'MGTS'")
    )
    if not result.fetchone():
        logger.info("舊 MGTS 資料庫不存在，跳過遷移")
        return

    for old_table, new_table in MGTS_MIGRATION_MAP.items():
        row_count = conn_server.execute(
            text(f"SELECT COUNT(*) FROM `MGTS`.`{old_table}`")
        ).scalar()

        if row_count == 0:
            logger.info("MGTS.%s 無資料，跳過", old_table)
            continue

        if old_table == new_table:
            conn_server.execute(
                text(f"INSERT IGNORE INTO `TWSE`.`{new_table}` "
                     f"SELECT * FROM `MGTS`.`{old_table}`")
            )
            conn_server.commit()
            logger.info("已從 MGTS.%s 以 INSERT IGNORE 合併至 TWSE.%s",
                         old_table, new_table)
            continue

        target_count = conn_server.execute(
            text(f"SELECT COUNT(*) FROM `TWSE`.`{new_table}`")
        ).scalar()

        if target_count > 0:
            logger.info("TWSE.%s 已有 %d 筆資料，跳過遷移", new_table, target_count)
            continue

        conn_server.execute(
            text(f"INSERT INTO `TWSE`.`{new_table}` "
                 f"SELECT * FROM `MGTS`.`{old_table}`")
        )
        conn_server.commit()
        logger.info("已從 MGTS.%s 搬移 %d 筆資料至 TWSE.%s",
                     old_table, row_count, new_table)

    conn_server.execute(text("DROP DATABASE `MGTS`"))
    conn_server.commit()
    logger.info("已刪除舊 MGTS 資料庫")


def main(opt):
    """建立資料庫與資料表的主函式。

    Args:
        opt: 命令列參數，包含 host、user、password。
    """
    HOST = opt.host
    USER = opt.user
    PASSWORD = opt.password

    all_subclasses = build_DB.BaseBuild.__subclasses__()
    conn_server = MySQLRouter(HOST, USER, PASSWORD).mysql_conn

    for subclass in all_subclasses:
        build_DB_obj = subclass()
        build_DB_obj.build_db(conn_server)
        conn_db = MySQLRouter(HOST, USER, PASSWORD, build_DB_obj.name).mysql_conn
        build_DB_obj.build_table(conn_db)
        conn_db.close()

    consolidate_mgts_tables(conn_server)
    migrate_mgts_to_twse(conn_server)

    conn_server.close()
    logger.info("所有資料庫與資料表建立完成")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
        handlers=[
            logging.FileHandler("logs/build_db.log"),
            logging.StreamHandler(),
        ],
    )
    parser = argparse.ArgumentParser(description="Build the database and tables.")
    parser.add_argument("--host", type=str, default="tw_stock_database", help="Database host")
    parser.add_argument("--user", type=str, default="root", help="Database user")
    parser.add_argument("--password", type=str, default="stock", help="Database password")
    opt = parser.parse_args()
    main(opt)
    