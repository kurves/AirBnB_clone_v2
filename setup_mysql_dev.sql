-- create databaseh
-- if it doesn't exist
CREATE DATABASE IF NOT EXISTS hbnb_dev_db;
-- create user
-- if user doesn't exist
CREATE USER IF NOT EXISTS 'hbnb_dev'@'localhost' IDENTIFIED BY 'hbnb_dev_pwd';
-- grant privileges to user
-- to user
GRANT ALL PRIVILEGES ON hbnb_dev_db.* TO 'hbnb_dev'@'localhost';
-- grant perfomance select
-- to usser
GRANT SELECT ON performance_schema.* TO 'hbnb_dev'@'localhost';
