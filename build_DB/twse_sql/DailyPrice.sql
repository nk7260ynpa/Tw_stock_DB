CREATE TABLE `TWSE`.`DailyPrice` (
    `Date` DATE NOT NULL,
    `SecurityCode` VARCHAR(10) NOT NULL,
    `TradeVolume` BIGINT NOT NULL,
    `Transaction` INT NOT NULL,
    `TradeValue` BIGINT NOT NULL,
    `OpeningPrice` DECIMAL(7,2) NOT NULL,
    `HighestPrice` DECIMAL(7,2) NOT NULL,
    `LowestPrice` DECIMAL(7,2) NOT NULL,
    `ClosingPrice` DECIMAL(7,2) NOT NULL,
    `Change` DECIMAL(7,2) NOT NULL,
    `LastBestBidPrice` DECIMAL(7,2) NOT NULL,
    `LastBestBidVolume` BIGINT NOT NULL,
    `LastBestAskPrice` DECIMAL(7,2) NOT NULL,
    `LastBestAskVolume` BIGINT NOT NULL,
    `PriceEarningratio` DECIMAL(7,2) NOT NULL,
    PRIMARY KEY (`Date`, `SecurityCode`)
)