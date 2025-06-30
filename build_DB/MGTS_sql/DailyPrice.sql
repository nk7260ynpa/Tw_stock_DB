CREATE TABLE `MGTS`.`DailyPrice` (
    `Date` DATE NOT NULL,
    `SecurityCode` VARCHAR(10) NOT NULL,
    `MarginSales` INT,
    `CashRedemption` INT,
    `MarginPurchaseBalanceOfPreviousDay` INT,
    `MarginPurchaseBalanceOfTheDay` INT,
    `MarginPurchaseQuotaForTheNextDay` INT,
    `ShortCovering` INT,
    `ShortSale` INT,
    `StockRedemption` INT,
    `ShortSaleBalanceOfPreviousDay` INT,
    `ShortSaleBalanceOfTheDay` INT,
    `ShortSaleQuotaForTheNextDay` INT,
    `OffsettingOfMarginPurchasesAndShortSales` INT,
    `Note` VARCHAR(10),
    PRIMARY KEY (`Date`, `SecurityCode`)
)