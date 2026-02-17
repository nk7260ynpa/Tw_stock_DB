# DB_builder

台灣股市資料庫建構工具，用於建立 MySQL 資料庫與資料表。

## 使用方式

### 快速啟動
```bash
bash run.sh
```

### 手動操作

#### 1. 啟動 SQL DB Server
```bash
# 建立 DB docker network
docker network create db_network
```
啟動 DB
```bash
docker compose -f docker/TwDatabase.yaml up -d
```

#### 2. 建立資料庫
```bash
docker run --rm --network db_network -v $(pwd)/logs:/workspace/logs nk7260ynpa/dbmaker:1.0.0
```

## 單元測試
```bash
# 執行所有測試
docker run --rm nk7260ynpa/dbmaker:1.0.0 python -m pytest test/

# 執行特定測試檔案
docker run --rm nk7260ynpa/dbmaker:1.0.0 python -m pytest test/test_build_DB/test_base.py

# 顯示詳細測試結果
docker run --rm nk7260ynpa/dbmaker:1.0.0 python -m pytest test/ -v
```

## 建立 Docker Image
```bash
bash docker/build.sh
```

## CHANGE LOG
- 2025/12/01: 將mysql:8.3 設為 nk7260ynpa/tw_stock_database:1.0.0
- 2025/12/01: 將phpmyadmin:5.2.1 設為 nk7260ynpa/db_manager:1.0.0
- 2025/12/01: 刪除 docker volume 設定
- 2025/12/02: 使用docker container 取代原生環境
- 2025/12/03: 將建立docker image 指令改到 README.md
- 2025/12/04: 調整建立資料庫指令
- 2026/02/17: 移除上傳與爬蟲相關功能，僅保留建立 DB 功能
- 2026/02/17: 移除 phpmyadmin 服務
- 2026/02/17: 將 MySQL image 升級為 mysql:9.6.0，移除已廢棄的 authentication plugin 參數
- 2026/02/17: 新增 run.sh、docker/build.sh、logs/，將 print 改為 logging
