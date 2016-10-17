create database IF NOT EXISTS crossoverproject;

use crossoverproject;

create table  IF NOT EXISTS clientstats (
ID int NOT NULL AUTO_INCREMENT,
username varchar(255),
timestamp varchar(255),
hostname varchar(255),
IPAddress varchar(255) not NULL,
CPUCount char(2),
CPUUsage varchar(255),
MemoryUsage varchar(255),
Uptime varchar(255),
primary key(ID));