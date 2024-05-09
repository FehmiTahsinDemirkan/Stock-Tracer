-- Veritabanını oluştur
CREATE DATABASE StockTracer;
GO

-- StockTracer veritabanını kullan
USE StockTracer;
GO

-- Users tablosunu oluştur
CREATE TABLE Users (
    id INT PRIMARY KEY IDENTITY,
    first_name NVARCHAR(50) NOT NULL,
    last_name NVARCHAR(50) NOT NULL,
    phone_number NVARCHAR(20),
    email NVARCHAR(100) NOT NULL,
    password NVARCHAR(100) NOT NULL
);
GO

-- Product tablosunu oluştur
CREATE TABLE Product (
    id INT PRIMARY KEY IDENTITY,
    product_name VARCHAR(255),
    category VARCHAR(255),
    expiration_date DATE,
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES Users(id)
);

GO
