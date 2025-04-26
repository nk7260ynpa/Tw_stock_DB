CREATE TABLE `TWSE`.`DailyPrice` (
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
);

CREATE TABLE `TWSE`.`StockName` (
    `SecurityCode` VARCHAR(10) NOT NULL,
    `StockName` VARCHAR(15) NOT NULL,
    PRIMARY KEY (`SecurityCode`)
);

CREATE TABLE `TWSE`.`Translate` (
    `English` VARCHAR(10) NOT NULL,
    `Chinese` VARCHAR(15) NOT NULL,
    PRIMARY KEY (`English`)
);