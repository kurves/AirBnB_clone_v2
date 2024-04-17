-- create databaseh
-- if it doesn't exist
CREATE DATABASE IF NOT EXISTS hbnb_test_db;
-- create user
-- if user doesn't exist
CREATE USER IF NOT EXISTS 'hbnb_test'@'localhost' IDENTIFIED BY 'hbnb_test_pwd';
-- grant privileges to user
-- to user
GRANT ALL PRIVILEGES ON hbnb_test_db.* TO 'hbnb_test'@'localhost';
-- grant perfomance select
-- to usser
GRANT SELECT ON performance_schema.* TO 'hbnb_test'@'localhost';
