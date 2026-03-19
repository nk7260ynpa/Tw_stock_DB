CREATE TABLE `SPECIAL_INFO`.`CurrencyPrice` (
    `Date` DATE NOT NULL,
    `Product` VARCHAR(10) NOT NULL COMMENT '匯率類型: USDTWD, USDJPY 等',
    `Open` DECIMAL(10, 4) COMMENT '開盤價',
    `High` DECIMAL(10, 4) COMMENT '最高價',
    `Low` DECIMAL(10, 4) COMMENT '最低價',
    `Close` DECIMAL(10, 4) COMMENT '收盤價',
    `Volume` BIGINT COMMENT '成交量',
    PRIMARY KEY (`Date`, `Product`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='國際匯率價格';
