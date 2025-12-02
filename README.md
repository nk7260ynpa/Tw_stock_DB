# DB_builder

# 1. 建立資料庫
## 啟動SQL DB Server
```bash
# 建立 DB docker network
docker network create db_network
```
啟動 DB
```bash
docker compose -f docker/TwDatabase.yaml up -d
```

## 建立資料庫
```bash
# 建立股市資料庫
docker run --network db_network nk7260ynpa/dbmaker:1.0.0
```

## 啟動爬蟲 server
```bash
docker compose -f docker/docker-compose.yml up -d
```

## 爬蟲資料庫
```bash
python upload.py --date {日期}
```

# 2. 建立 docker image
## 建立 DB maker image
```bash
docker build -f docker/DBmaker -t nk7260ynpa/dbmaker:1.0.0 .
```

## 建立 每日爬蟲 image
```bash
docker build -f docker/Dockerfile -t nk7260ynpa/tw_stocker_daily_process:1.0.1 .
```

CHANGE LOG:
- 2025/12/01: 將mysql:8.3 設為 nk7260ynpa/tw_stock_database:1.0.0
- 2025/12/01: 將phpmyadmin:5.2.1 設為 nk7260ynpa/db_manager:1.0.0
- 2025/12/01: 刪除 docker volume 設定
- 2025/12/02: 使用docker container 取代原生環境
- 2025/12/03: 更新每日爬蟲時間