CREATE TABLE `weatherdata` (
  `year` varchar(4) NOT NULL,
  `month` varchar(2) NOT NULL,
  `day` varchar(2) NOT NULL,
  `site` varchar(50) NOT NULL,
  `water_termperature` varchar(2) DEFAULT NULL,
  `f1` int(3) DEFAULT NULL,
  `descripcion1` varchar(30) DEFAULT NULL,
  `f2` int(3) DEFAULT NULL,
  `descripcion2` varchar(30) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

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
  `earth_temperature` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;



ALTER TABLE `weatherdata`
  ADD PRIMARY KEY (`year`,`month`,`day`,`site`);


ALTER TABLE `windconditions`
  ADD PRIMARY KEY (`year`,`month`,`day`,`time_of_day`,`site`);
COMMIT;
