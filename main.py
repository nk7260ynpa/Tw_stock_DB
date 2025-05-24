import build_DB
from clients import mysql_conn, mysql_conn_db


# 獲取所有繼承 BaseBuild 的子類別
all_subclasses = build_DB.BaseBuild.__subclasses__()

host = "localhost:3306"
user = "root"
password = "stock"
conn_server = mysql_conn(host, user, password)
bui = all_subclasses[0]()
bui.build_db(conn_server)
conn_server.close()
conn_db = mysql_conn_db(host, user, password, bui.name)
bui.build_table(conn_db)


    