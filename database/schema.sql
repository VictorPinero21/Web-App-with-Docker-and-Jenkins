CREATE DATABASE IF NOT EXISTS two_tier_app;

USE two_tier_app;

CREATE TABLE IF NOT EXISTS messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    message TEXT NOT NULL
);
