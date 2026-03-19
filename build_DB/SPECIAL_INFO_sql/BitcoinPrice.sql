CREATE TABLE `SPECIAL_INFO`.`BitcoinPrice` (
    `Date` DATE NOT NULL,
    `Product` VARCHAR(10) NOT NULL COMMENT '加密貨幣類型: BTC',
    `Open` DECIMAL(12, 2) COMMENT '開盤價',
    `High` DECIMAL(12, 2) COMMENT '最高價',
    `Low` DECIMAL(12, 2) COMMENT '最低價',
    `Close` DECIMAL(12, 2) COMMENT '收盤價',
    `Volume` BIGINT COMMENT '成交量',
    PRIMARY KEY (`Date`, `Product`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='比特幣價格';
