# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 專案概述

台灣股市資料庫建構工具，建立 5 個 MySQL 資料庫（TWSE、TPEX、TAIFEX、FAOI、MGTS），每個資料庫包含 DailyPrice、StockName、Translate、UploadDate 四張資料表。所有程式碼皆在 Docker container 中執行。

## 常用指令

```bash
# 一鍵啟動（建立網路 → 啟動 MySQL → 等待就緒 → 建立資料庫）
bash run.sh

# 建立 DBmaker Docker image
bash docker/build.sh

# 啟動 MySQL Server
docker network create db_network
docker compose -f docker/TwDatabase.yaml up -d

# 執行資料庫建構
docker run --rm --network db_network nk7260ynpa/dbmaker:1.0.0

# 執行測試
docker run --rm nk7260ynpa/dbmaker:1.0.0 python -m pytest test/
```

## 架構

```
main.py  →  routers.py (MySQLRouter)  →  clients.py (SQLAlchemy+pymysql)
   ↓
build_DB/
├── base.py          # 核心抽象：BuildEmptyDB、BaseBuildTABLE、BaseBuild
├── twse.py          # 各資料庫的具體實作（twse/tpex/taifex/faoi/mgts）
└── *_sql/           # SQL 定義檔 + CSV 初始數據
```

**關鍵設計模式：**
- `main.py` 透過 `BaseBuild.__subclasses__()` 自動發現所有資料庫建構類（Factory pattern）
- `BaseBuildTABLE.build()` 呼叫抽象方法 `post_process()` 執行初始數據匯入（Template Method）
- 類別命名規則決定 SQL 檔案路徑：`BuildTWSETABLEDailyPrice` → `build_DB/TWSE_sql/DailyPrice.sql`

## 新增資料庫的方式

1. 在 `build_DB/` 建立 `newdb.py`，繼承 `BaseBuild` 和 `BaseBuildTABLE`
2. 在 `build_DB/NEWDB_sql/` 放置 `db.sql`、各資料表 `.sql` 和 `.csv` 初始數據
3. 在 `build_DB/__init__.py` 匯出新類別
4. `main.py` 會自動偵測並建構

## Docker 環境

- **MySQL**：`mysql:9.6.0`，container 名稱 `tw_stock_database`，使用 healthcheck 確認就緒
- **DBmaker**：`nk7260ynpa/dbmaker:1.0.0`，基於 Python 3.12.7
- **網路**：external network `db_network`
- **資料持久化**：`StockDB/` 目錄（已被 .gitignore 忽略）
- **預設連線**：host=tw_stock_database, user=root, password=stock

## 日誌

使用 Python `logging` 模組，同時輸出至 `logs/build_db.log` 與標準輸出。
