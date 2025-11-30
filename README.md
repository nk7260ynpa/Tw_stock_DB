# DB_builder

# 1. 建立資料庫
## 啟動SQL DB Server
```bash
# 建立 DB docker volume
docker volume create StockDB
docker network create db_network
```
啟動 DB
```bash
docker compose -f docker/TwDatabase.yaml up -d
```

## 建立資料庫
```bash
# 建立股市資料庫
python main.py
```

## 啟動爬蟲 server
```bash
docker compose -f docker/docker-compose.yml up -d
```

## 爬蟲資料庫
```bash
python upload.py --date {日期}
```
