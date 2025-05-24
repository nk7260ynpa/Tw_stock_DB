import build_DB
from router import MySQLRouter

def main(opt):
    # 獲取所有繼承 BaseBuild 的子類別
    all_subclasses = build_DB.BaseBuild.__subclasses__()

    host = "localhost:3306"
    user = "root"
    password = "stock"
    conn_server = MySQLRouter(host, user, password).mysql_conn
    bui = all_subclasses[0]()
    bui.build_db(conn_server)
    conn_server.close()
    conn_db = MySQLRouter(host, user, password, bui.name).mysql_conn
    bui.build_table(conn_db)
    conn_db.close()


    