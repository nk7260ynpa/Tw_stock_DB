CREATE TABLE `TWSE`.`CompanyInfo` (
    `SecurityCode` VARCHAR(10) NOT NULL,
    `IndustryCode` VARCHAR(5) DEFAULT NULL,
    `Industry` VARCHAR(20) DEFAULT NULL,
    `CompanyName` VARCHAR(50) DEFAULT NULL,
    `SpecialShares` BIGINT DEFAULT NULL,
    `NormalShares` BIGINT DEFAULT NULL,
    `PrivateShares` BIGINT DEFAULT NULL,
    PRIMARY KEY (`SecurityCode`)
)