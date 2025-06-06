-- Create the database
CREATE DATABASE IF NOT EXISTS sms1;
USE sms1;

-- Create the 'data' table to store student details
CREATE TABLE IF NOT EXISTS data (
    rollno VARCHAR(20) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    course VARCHAR(100) NOT NULL,
    dob VARCHAR(20) NOT NULL,
    gender VARCHAR(10) NOT NULL,
    contact VARCHAR(20) NOT NULL,
    email VARCHAR(100),
    address VARCHAR(255)
);
