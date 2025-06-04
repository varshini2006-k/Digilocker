# Digilocker

-- Create Database
CREATE DATABASE digilocker;
USE digilocker;

-- Create Users Table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE
);

-- Create Documents Table
CREATE TABLE documents (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    document_name VARCHAR(255) NOT NULL,
    file_path VARCHAR(255) NOT NULL,
    file_size INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Create Shared Documents Table
CREATE TABLE shared_documents (
    id INT AUTO_INCREMENT PRIMARY KEY,
    document_id INT NOT NULL,
    shared_with_email VARCHAR(255) NOT NULL,
    FOREIGN KEY (document_id) REFERENCES documents(id)
);

-- Create Recently Viewed Table
CREATE TABLE recently_viewed (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    document_id INT NOT NULL,
    viewed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (document_id) REFERENCES documents(id)
);
-- Retrieve all users from the 'users' table
-- This query fetches all registered users along with their login credentials and email addresses.
SELECT * FROM users;

-- Retrieve all uploaded documents from the 'documents' table
-- This query fetches every document uploaded by users, including document name, path, size, and associated user.
SELECT * FROM documents;

-- Retrieve all shared documents from the 'shared_documents' table
-- This query lists all documents that have been shared along with the recipient email addresses.
SELECT * FROM shared_documents;

-- Retrieve all recently viewed documents from the 'recently_viewed' table
-- This query returns the history of documents viewed by users, including timestamps of when they were accessed.
SELECT * FROM recently_viewed;



