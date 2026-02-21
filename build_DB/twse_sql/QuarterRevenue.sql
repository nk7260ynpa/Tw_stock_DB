CREATE TABLE `TWSE`.`QuarterRevenue` (
    `SecurityCode` VARCHAR(10) NOT NULL,
    `Year` YEAR NOT NULL,
    `Quarter` VARCHAR(2) NOT NULL,
    `EPS` DECIMAL(10,2) DEFAULT NULL,
    `Revenue` BIGINT DEFAULT NULL,
    `Income` BIGINT DEFAULT NULL,
    `OtherIncome` BIGINT DEFAULT NULL,
    `NetIncome` BIGINT DEFAULT NULL,
    PRIMARY KEY (`SecurityCode`, `Year`, `Quarter`)
)