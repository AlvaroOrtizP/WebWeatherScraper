CREATE TABLE `wind_conditions` (
  `year` varchar(4) NOT NULL,
  `month` int(2) NOT NULL,
  `day` int(2) NOT NULL,
  `site` varchar(50) NOT NULL,
  `time_of_day` varchar(30) NOT NULL,
  `wind` int(11) DEFAULT NULL,
  `wind_direction` decimal(5,2) DEFAULT NULL,
  `gusts_of_wind` double DEFAULT NULL,
  `wave_height` varchar(5) NOT NULL,
  `wave_period` int(11) DEFAULT NULL,
  `earth_temperature` int(11) DEFAULT NULL,
  `water_temperature` varchar(2) NOT NULL,
  `condition_code` int(3) NOT NULL,
  `condition_description` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


ALTER TABLE `wind_conditions`
  ADD PRIMARY KEY (`year`,`month`,`day`,`time_of_day`,`site`);



CREATE TABLE `configuration_data` (
  `id` int(11) NOT NULL,
  `ID_WINDWURU` int(11) NOT NULL,
  `ID_AEMET` varchar(30) NOT NULL,
  `ID_PLAYA` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

ALTER TABLE `configuration_data`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

INSERT INTO `configuration_data` (`id`, `ID_WINDWURU`, `ID_AEMET`, `ID_PLAYA`) VALUES
(1, 487006, 'play_v2_3900602', 'Ajo,Cantabria');





CREATE TABLE `tide_table` (
  `day` varchar(4) NOT NULL,
  `month` varchar(2) NOT NULL,
  `year` varchar(2) NOT NULL,
  `site` varchar(50) NOT NULL,
  `moon_phase` int(4) NOT NULL,
  `coefficient0H` int(3) NOT NULL,
  `coefficient12H` int(3) NOT NULL,
  `morning_high_tide_time` varchar(5) NOT NULL,
  `morning_high_tide_height` decimal(2,2) NOT NULL,
  `afternoon_high_tide_time` varchar(5) NOT NULL,
  `afternoon_high_tide_height` decimal(2,2) NOT NULL,
  `morning_low_tide_time` varchar(5) NOT NULL,
  `morning_low_tide_height` decimal(2,2) NOT NULL,
  `afternoon_low_tide_time` varchar(5) NOT NULL,
  `afternoon_low_tide_height` decimal(2,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

ALTER TABLE `tide_table`
  ADD PRIMARY KEY (`day`,`month`,`year`,`site`);


