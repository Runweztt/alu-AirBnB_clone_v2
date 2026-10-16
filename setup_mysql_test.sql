-- Prepare the MySQL test database for AirBnB clone v2
CREATE DATABASE IF NOT EXISTS hbnb_test_db;

-- Create the test user
CREATE USER IF NOT EXISTS 'hbnb_test'@'localhost'
IDENTIFIED BY 'hbnb_test_pwd';

-- Grant all privileges on the test database
GRANT ALL PRIVILEGES ON hbnb_test_db.*
TO 'hbnb_test'@'localhost';

-- Grant SELECT privilege on performance_schema
GRANT SELECT ON performance_schema.*
TO 'hbnb_test'@'localhost';

-- Apply privilege changes
FLUSH PRIVILEGES;
