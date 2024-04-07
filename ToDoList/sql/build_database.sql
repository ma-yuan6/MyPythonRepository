DROP DATABASE IF EXISTS todo;
CREATE DATABASE todo;

USE todo;

CREATE TABLE topic (
    id int PRIMARY KEY,
    title varchar(255) NOT NULL,
    link varchar(255) NOT NULL,
    start_time date NOT NULL,
    day_1 tinyint(1) NOT NULL DEFAULT 0,
	time_1 datetime,
	day_2 tinyint(1) NOT NULL DEFAULT 0,
	time_2 datetime,
	day_4 tinyint(1) NOT NULL DEFAULT 0,
	time_4 datetime,
	day_7 tinyint(1) NOT NULL DEFAULT 0,
	time_7 datetime,
	day_15 tinyint(1) NOT NULL DEFAULT 0,
	time_15 datetime,
	day_30 tinyint(1) NOT NULL DEFAULT 0,
	time_30 datetime,
	day_90 tinyint(1) NOT NULL DEFAULT 0,
	time_90 datetime,
	day_180 tinyint(1) NOT NULL DEFAULT 0,
	time_180 DATETIME
);

CREATE TABLE modified_records (
    topic_id int NOT NULL,
	modified_time datetime NOT NULL,
	day varchar(16) NOT NULL
);
