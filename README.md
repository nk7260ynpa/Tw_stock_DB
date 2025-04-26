# DB_builder

安裝爬蟲套件
```bash
pip install -r https://github.com/nk7260ynpa/tw_stock_crawer/requirements.txt
pip install git+https://github.com/nk7260ynpa/tw_stock_crawer.git
```

# 建立資料庫
## 啟動SQL DB Server
```bash
# 建立 DB docker volume
docker volume create StockDB
```
啟動 DB
```bash
docker compose -f TwDatabase.yaml up -d
```

## 建立資料庫
```bash
# 建立TWSE、TPEX、TAIFEX資料庫
python build_db.py
```


