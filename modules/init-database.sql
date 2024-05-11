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

CREATE TABLE NotificationUsers (
    id INT PRIMARY KEY IDENTITY,
    email NVARCHAR(100) NOT NULL
);

GO
--Tablodaki ürünlerin son kullanma tarihine 1 ve 1 haftadan az kalmış ürünleri ExpiringProducts tablosuna kaydetmek
INSERT INTO ExpiringProducts (product_name, expiration_date, user_id)
SELECT product_name, expiration_date, user_id
FROM Product
WHERE expiration_date <= DATEADD(DAY, 1, GETDATE()) -- Son kullanma tarihi 1 gün veya daha az kalanlar
   OR expiration_date <= DATEADD(DAY, 7, GETDATE()); -- Son kullanma tarihi 1 hafta veya daha az kalanlar


