import argparse
import logging

import build_DB
from routers import MySQLRouter

logger = logging.getLogger(__name__)


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
    