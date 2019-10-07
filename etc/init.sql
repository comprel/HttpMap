
DROP TABLE IF EXISTS `example`;

CREATE TABLE `example` (
  `id` VARCHAR(36) NOT NULL,
  `name` VARCHAR(255) DEFAULT NULL,
  `task_id` VARCHAR(36) DEFAULT NULL,
  `created_time` DATETIME DEFAULT NULL,
  `updated_time` DATETIME DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=INNODB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `host`;

CREATE TABLE `host` (
  `id` varchar(64) NOT NULL,
  `hostname` varchar(255) DEFAULT NULL,
  `ipaddress` varchar(36) DEFAULT NULL,
  `uname` varchar(128) DEFAULT NULL,
  `version` varchar(32) DEFAULT NULL,
  `created_time` datetime DEFAULT NULL,
  `updated_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_hostname` (`hostname`),
  KEY `idx_ipaddress` (`ipaddress`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `ipaddress`;

CREATE TABLE `ipaddress` (
  `ip` varchar(64) NOT NULL,
  `host_id` varchar(64) DEFAULT NULL,
  `created_time` datetime DEFAULT NULL,
  `updated_time` datetime DEFAULT NULL,
  PRIMARY KEY (`ip`),
  KEY `idx_host` (`host_id`)
  UNIQUE KEY `idx_host_ip` (`ip`, `host_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

