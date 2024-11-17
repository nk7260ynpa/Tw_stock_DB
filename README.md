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