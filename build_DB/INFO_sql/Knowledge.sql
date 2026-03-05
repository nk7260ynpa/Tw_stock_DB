CREATE TABLE `INFO`.`Knowledge` (
    `id` INT AUTO_INCREMENT,
    `category` VARCHAR(50) NOT NULL,
    `term` VARCHAR(100) NOT NULL,
    `description` TEXT NOT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_category_term` (`category`, `term`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
