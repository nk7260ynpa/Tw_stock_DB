CREATE TABLE `TPEX` . `DailyPrice` (
    `Date` DATE NOT NULL,
	`Code` VARCHAR(10) NOT NULL,
	`Close` DECIMAL(10, 2) NOT NULL,
    `Open` DECIMAL(10, 2) NOT NULL,
    `High` DECIMAL(10, 2) NOT NULL,
    `Low` DECIMAL(10, 2) NOT NULL,
    `TradeVol(shares)` DECIMAL(10, 2) NOT NULL,
    `TradeAmt.(NTD)` DECIMAL(12, 2) NOT NULL,
    `No.ofTransactions` DECIMAL(10, 2) NOT NULL,
    `LastBestBidPrice` DECIMAL(10, 2) NOT NULL,
    `LastBidVolume` DECIMAL(10, 2) NOT NULL,
    `LastBestAskPrice` DECIMAL(10, 2) NOT NULL,
    `LastBestAskVolume` DECIMAL(10, 2) NOT NULL,
    `IssuedShares` DECIMAL(10, 2) NOT NULL,
    `NextDayUp-LimitPrice` DECIMAL(10, 2) NOT NULL,
    `NextDayDown-LimitPrice` DECIMAL(10, 2) NOT NULL,
    PRIMARY KEY (`Date`, `Code`)
)