CREATE TABLE `TWSE`.`TDCC` (
    `Date` DATE NOT NULL,
    `SecurityCode` VARCHAR(10) NOT NULL,
    `Level` INT NOT NULL,
    `Holders` INT NOT NULL,
    `HoldingShares` BIGINT NOT NULL,
    `HoldingRatio` DECIMAL(6,2) NOT NULL,
    PRIMARY KEY (`Date`, `SecurityCode`, `Level`)
)
