CREATE TABLE `TWSE`.`StockName` (
    `SecurityCode` VARCHAR(10) NOT NULL,
    `StockName` VARCHAR(15) NOT NULL,
    `CompanyName` VARCHAR(50) DEFAULT NULL,
    `IndustryCode` VARCHAR(5) DEFAULT NULL,
    `Industry` VARCHAR(20) DEFAULT NULL,
    `NormalShares` BIGINT DEFAULT NULL,
    `PrivateShares` BIGINT DEFAULT NULL,
    `SpecialShares` BIGINT DEFAULT NULL,
    PRIMARY KEY (`SecurityCode`)
)