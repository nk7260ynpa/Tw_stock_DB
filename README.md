# DB_builder

# 1. 建立資料庫
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
# 建立TWSE資料庫
python main.py
```
