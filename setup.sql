CREATE DATABASE IF NOT EXISTS exhibia;
CREATE USER 'exhibia'@'localhost' IDENTIFIED BY '$$nrule2020';
GRANT ALL PRIVILEGES ON exhibia.* TO 'exhibia'@'localhost' WITH GRANT OPTION;

