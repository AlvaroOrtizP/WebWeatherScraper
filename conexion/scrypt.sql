CREATE TABLE `windconditions` (
  `year` varchar(4) NOT NULL,
  `month` varchar(2) NOT NULL,
  `day` varchar(2) NOT NULL,
  `site` varchar(50) NOT NULL,
  `time_of_day` varchar(30) NOT NULL,
  `wind` int(11) DEFAULT NULL,
  `wind_direction` decimal(5,2) DEFAULT NULL,
  `gusts_of_wind` double DEFAULT NULL,
  `wave_height` varchar(5) NOT NULL,
  `wave_period` int(11) DEFAULT NULL,
  `earth_temperature` int(11) DEFAULT NULL,
  `water_termperature` varchar(2) NOT NULL,
  `f1` int(3) NOT NULL,
  `descripcion1` varchar(30) NOT NULL,
  `f2` int(3) NOT NULL,
  `descripcion2` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;



ALTER TABLE `windconditions`
  ADD PRIMARY KEY (`year`,`month`,`day`,`time_of_day`,`site`);
COMMIT;

CREATE TABLE `configuration_data` (
  `id` int(11) NOT NULL,
  `ID_WINDWURU` int(11) NOT NULL,
  `ID_AEMET` varchar(30) NOT NULL,
  `ID_PLAYA` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

ALTER TABLE `configuration_data`
  ADD PRIMARY KEY (`id`);
