-- Create the development database with a compatible character set.
CREATE DATABASE IF NOT EXISTS hbnb_dev_db
CHARACTER SET latin1
COLLATE latin1_swedish_ci;

-- Create the development MySQL user.
CREATE USER IF NOT EXISTS 'hbnb_dev'@'localhost'
IDENTIFIED BY 'hbnb_dev_pwd';

-- Grant all privileges on the development database.
GRANT ALL PRIVILEGES ON hbnb_dev_db.*
TO 'hbnb_dev'@'localhost';

-- Grant read access to performance_schema.
GRANT SELECT ON performance_schema.*
TO 'hbnb_dev'@'localhost';
