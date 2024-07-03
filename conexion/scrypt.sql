CREATE TABLE `configuration_data` (
  `id` int NOT NULL AUTO_INCREMENT,
  `ID_WINDWURU` int NOT NULL,
  `ID_AEMET` varchar(30) COLLATE utf8mb4_general_ci NOT NULL,
  `ID_PLAYA` varchar(30) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`)


) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
INSERT INTO configuration_data (ID_WINDWURU, ID_AEMET, ID_PLAYA)
VALUES ('487006', 'play_v2_3900602', 'Ajo,Cantabria');

CREATE TABLE `dive_day` (
  `dive_day_id` int NOT NULL AUTO_INCREMENT,
  `day` varchar(2) COLLATE utf8mb4_general_ci NOT NULL,
  `beginning` varchar(2) COLLATE utf8mb4_general_ci NOT NULL,
  `end` varchar(2) COLLATE utf8mb4_general_ci NOT NULL,
  `site` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `notes` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `year` varchar(4) COLLATE utf8mb4_general_ci NOT NULL,
  `month` varchar(2) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`dive_day_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `fish` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(60) COLLATE utf8mb4_general_ci NOT NULL,
  `first_sighting` date NOT NULL,
  `first_last` date NOT NULL,
  `start_season` date NOT NULL,
  `end_season` date NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


CREATE TABLE `fishing` (
  `id` int NOT NULL AUTO_INCREMENT,
  `fish_id` int NOT NULL, 
  `notes` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `caught` tinyint(1) NOT NULL,
  `weight` decimal(2,2) NOT NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`fish_id`) REFERENCES `fish`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


CREATE TABLE `tide_table` (
  `day` varchar(2) COLLATE utf8mb4_general_ci NOT NULL,
  `month` varchar(2) COLLATE utf8mb4_general_ci NOT NULL,
  `year` varchar(4) COLLATE utf8mb4_general_ci NOT NULL,
  `site` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `moon_phase` int NOT NULL,
  `coefficient0H` int NOT NULL,
  `coefficient12H` int NOT NULL,
  `morning_high_tide_time` varchar(5) COLLATE utf8mb4_general_ci NOT NULL,
  `morning_high_tide_height` varchar(5) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `afternoon_high_tide_time` varchar(5) COLLATE utf8mb4_general_ci NOT NULL,
  `afternoon_high_tide_height` varchar(5) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `morning_low_tide_time` varchar(5) COLLATE utf8mb4_general_ci NOT NULL,
  `morning_low_tide_height` varchar(5) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `afternoon_low_tide_time` varchar(5) COLLATE utf8mb4_general_ci NOT NULL,
  `afternoon_low_tide_height` varchar(5) COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`day`,`month`,`year`,`site`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;



CREATE TABLE `wind_conditions` (
  `year` varchar(4) COLLATE utf8mb4_general_ci NOT NULL,
  `month` int NOT NULL,
  `day` int NOT NULL,
  `site` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `time_of_day` varchar(30) COLLATE utf8mb4_general_ci NOT NULL,
  `wind` int DEFAULT NULL,
  `wind_direction` decimal(5,2) DEFAULT NULL,
  `gusts_of_wind` double DEFAULT NULL,
  `wave_height` varchar(5) COLLATE utf8mb4_general_ci NOT NULL,
  `wave_period` int DEFAULT NULL,
  `earth_temperature` int DEFAULT 0, 
  `water_temperature` varchar(2) COLLATE utf8mb4_general_ci ,
  `condition_code` int,
  `condition_description` varchar(30) COLLATE utf8mb4_general_ci ,
  PRIMARY KEY (`year`,`month`,`day`,`time_of_day`,`site`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


CREATE TABLE `dive_day_and_fishing` (
  `id_fishing` int NOT NULL,
  `dive_day_id` int NOT NULL,
  PRIMARY KEY (`id_fishing`,`dive_day_id`),
  KEY `fk_dive_day_id` (`dive_day_id`),
  CONSTRAINT `fk_dive_day_id` FOREIGN KEY (`dive_day_id`) REFERENCES `dive_day` (`dive_day_id`),
  CONSTRAINT `fk_fishing_id` FOREIGN KEY (`id_fishing`) REFERENCES `fishing` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;