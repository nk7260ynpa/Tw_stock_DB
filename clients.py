from abc import ABC, abstractmethod
from sqlalchemy import create_engine

def mysql_conn(host, user, password):
    address = f"mysql+pymysql://{user}:{password}@{host}"
    engine = create_engine(address)
    conn = engine.connect()
    return conn
