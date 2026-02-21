# DB_builder

台灣股市資料庫建構工具，建立 5 個 MySQL 資料庫（TWSE、TPEX、TAIFEX、FAOI、MGTS），
每個資料庫包含 DailyPrice、StockName、Translate、UploadDate 四張資料表。
TWSE 額外包含 CompanyInfo、IndustryMap、QuarterRevenue 和 QuarterRevenueUploaded 資料表。
所有程式碼皆在 Docker container 中執行。

## 專案架構

```
.
├── main.py                  # 主程式入口
├── routers.py               # MySQLRouter 連線路由
├── clients.py               # SQLAlchemy + pymysql 連線設定
├── run.sh                   # 一鍵啟動腳本
├── requirements.txt         # Python 套件依賴
├── build_DB/                # 資料庫建構模組
│   ├── base.py              # 核心抽象類別（BuildEmptyDB、BaseBuildTABLE、BaseBuild）
│   ├── twse.py              # TWSE 資料庫實作
│   ├── tpex.py              # TPEX 資料庫實作
│   ├── taifex.py            # TAIFEX 資料庫實作
│   ├── faoi.py              # FAOI 資料庫實作
│   ├── mgts.py              # MGTS 資料庫實作
│   └── *_sql/               # 各資料庫的 SQL 定義檔與 CSV 初始數據
├── docker/                  # Docker 相關設定
│   ├── build.sh             # 建立 Docker image 腳本
│   ├── Dockerfile           # Docker image 定義
│   └── TwDatabase.yaml      # MySQL docker compose 設定
├── test/                    # 單元測試
│   └── test_build_DB/
│       └── test_base.py     # base.py 單元測試
└── logs/                    # 日誌輸出目錄
```

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
- 2026/02/17: 新增 pytest 依賴、掛載 logs 至容器、強化單元測試驗證
- 2026/02/18: 將 MySQL image 改為 nk7260ynpa/mysql:9.6.0
- 2026/02/20: TWSE StockName 新增 CompanyName、IndustryCode、Industry 欄位
- 2026/02/20: 改進資料表建立邏輯，既有資料表可自動補上缺少的欄位（ALTER TABLE ADD COLUMN）
- 2026/02/21: TWSE StockName 新增 NormalShares、PrivateShares、SpecialShares 欄位
- 2026/02/21: TWSE 新增 CompanyInfo 資料表（公司基本資訊）
- 2026/02/21: TWSE StockName 移除公司相關欄位，改由 CompanyInfo 管理
- 2026/02/21: TWSE 新增 IndustryMap 資料表，將 Industry 從 CompanyInfo 獨立管理
- 2026/02/21: TWSE 新增 QuarterRevenue 資料表（季度營收資料）
