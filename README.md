# DB_builder

```bash
# 建立 DB docker volume
docker volume create StockDB
```
啟動 DB
```bash
docker compose -f TwDatabase.yaml up -d
```

## 建立資料庫

### 建立Taiwan Stock Exchange Database
```SQL
CREATE TABLE `TWSE` . `DailyPrice` (
    `Date` DATE NOT NULL,
	`SecurityCode` VARCHAR(10) NOT NULL,
	`StockName` VARCHAR(15) NOT NULL,
	`TradeVolume` BIGINT NOT NULL,
    `Transaction` INT NOT NULL,
    `TradeValue` BIGINT NOT NULL,
    `OpeningPrice` DECIMAL(7,2) NOT NULL,
    `HighestPrice` DECIMAL(7,2) NOT NULL,
    `LowestPrice` DECIMAL(7,2) NOT NULL,
    `ClosingPrice` DECIMAL(7,2) NOT NULL,
    `Change` DECIMAL(7,2) NOT NULL,
    `LastBestBidPrice` DECIMAL(7,2) NOT NULL,
    `LastBestBidVolume` INT NOT NULL,
    `LastBestAskPrice` DECIMAL(7,2) NOT NULL,
    `LastBestAskVolume` INT NOT NULL,
    `PriceEarningratio` DECIMAL(7,2) NOT NULL,
    PRIMARY KEY (`Date`, `SecurityCode`)
)
```

### 建立Over-the-Counter Exchange Database
```SQL
CREATE TABLE `TPEX` . `DailyPrice` (
    `Date` DATE NOT NULL,
	`Code` VARCHAR(10) NOT NULL,
	`Close` DECIMAL(10, 2) NOT NULL,
    `Open` DECIMAL(10, 2) NOT NULL,
    `High` DECIMAL(10, 2) NOT NULL,
    `Low` DECIMAL(10, 2) NOT NULL,
    `TradingVol(shares)` DECIMAL(10, 2) NOT NULL,
    `TradeAmt.(NTD)` DECIMAL(12, 2) NOT NULL,
    `No.ofTransactions` DECIMAL(10, 2) NOT NULL,
    `LastBidVolume` DECIMAL(10, 2) NOT NULL,
    PRIMARY KEY (`Date`, `SecurityCode`)
)