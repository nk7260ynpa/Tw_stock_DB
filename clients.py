from sqlalchemy import create_engine

def mysql_conn(host, user, password):
    address = f"mysql+pymysql://{user}:{password}@{host}"
    engine = create_engine(address)
    conn = engine.connect()
    return conn

def mysql_conn_db(host, user, password, db_name):
    address = f"mysql+pymysql://{user}:{password}@{host}/{db_name}"
    engine = create_engine(address)
    conn = engine.connect()
    return conn
