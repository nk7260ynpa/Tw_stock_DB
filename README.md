# DB_builder

台灣股市資料庫建構工具，用於建立 MySQL 資料庫與資料表。

## 使用方式

### 1. 啟動 SQL DB Server
```bash
# 建立 DB docker network
docker network create db_network
```
啟動 DB
```bash
docker compose -f docker/TwDatabase.yaml up -d
```

### 2. 建立資料庫
```bash
# 建立股市資料庫
docker run --rm --network db_network nk7260ynpa/dbmaker:1.0.0
```

## 建立 Docker Image

### 建立 DB maker image
```bash
docker build -f docker/DBmaker -t nk7260ynpa/dbmaker:1.0.0 .
```

## CHANGE LOG
- 2025/12/01: 將mysql:8.3 設為 nk7260ynpa/tw_stock_database:1.0.0
- 2025/12/01: 將phpmyadmin:5.2.1 設為 nk7260ynpa/db_manager:1.0.0
- 2025/12/01: 刪除 docker volume 設定
- 2025/12/02: 使用docker container 取代原生環境
- 2025/12/03: 將建立docker image 指令改到 README.md
- 2025/12/04: 調整建立資料庫指令
- 2026/02/17: 移除上傳與爬蟲相關功能，僅保留建立 DB 功能
