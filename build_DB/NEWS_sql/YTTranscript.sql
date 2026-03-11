CREATE TABLE `NEWS`.`YTTranscript` (
    `Date` DATE NOT NULL,
    `Title` VARCHAR(500) DEFAULT NULL,
    `url` VARCHAR(1000) NOT NULL,
    `Duration` VARCHAR(20) DEFAULT NULL,
    `ContentFile` VARCHAR(100) DEFAULT NULL,
    `Status` ENUM('success', 'failed', 'pending') DEFAULT 'pending',
    `ErrorMessage` VARCHAR(1000) DEFAULT NULL,
    PRIMARY KEY (`Date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
