--
-- Users table
--
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    affiliation VARCHAR(255) NOT NULL,
    status ENUM ('inactive', 'active', 'disabled') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    last_login TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

--
-- Plans table
-- maybe change the tiers to `free`, `premium`, 'enterprise'
--
-- CREATE TABLE IF NOT EXISTS plans (
--     id INT AUTO_INCREMENT PRIMARY KEY,
--     user_id
--     tier ENUM ('free', 'premium', 'enterprise') NOT NULL,
--     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
--     last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
-- );
