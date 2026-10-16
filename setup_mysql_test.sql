-- Create the test database with a compatible character set.
CREATE DATABASE IF NOT EXISTS hbnb_test_db
CHARACTER SET latin1
COLLATE latin1_swedish_ci;

-- Create the test MySQL user.
CREATE USER IF NOT EXISTS 'hbnb_test'@'localhost'
IDENTIFIED BY 'hbnb_test_pwd';

-- Grant all privileges on the test database.
GRANT ALL PRIVILEGES ON hbnb_test_db.*
TO 'hbnb_test'@'localhost';

-- Grant read access to performance_schema.
GRANT SELECT ON performance_schema.*
TO 'hbnb_test'@'localhost';
