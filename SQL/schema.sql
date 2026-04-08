/*
=============================================================
SCHEMA: Tables Creation
=============================================================
Purpose:
    Creates schemas and tables without constraints (except PKs & basic checks)
*/

USE ecommerce_db;
GO

-- Create Schemas (if not exist)
IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'crm')
    EXEC('CREATE SCHEMA crm');
GO

IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'inventory')
    EXEC('CREATE SCHEMA inventory');
GO

IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'sales')
    EXEC('CREATE SCHEMA sales');
GO


/* =========================
   CRM - Customers
========================= */
IF OBJECT_ID('crm.customers', 'U') IS NOT NULL
    DROP TABLE crm.customers;
GO

CREATE TABLE crm.customers (
    customer_id        INT             PRIMARY KEY,
    name               NVARCHAR(255)   NOT NULL,
    email              NVARCHAR(255)   NOT NULL,
    date_of_birth      DATE,
    address            NVARCHAR(500),
    phone_number       NVARCHAR(25),
    created_at         DATETIME2       DEFAULT CURRENT_TIMESTAMP
);
GO


/* =========================
   Inventory - Products
========================= */
IF OBJECT_ID('inventory.products', 'U') IS NOT NULL
    DROP TABLE inventory.products;
GO

CREATE TABLE inventory.products (
    product_id         NVARCHAR(50)    PRIMARY KEY,
    title              NVARCHAR(255)   NOT NULL,
    category           NVARCHAR(255),
    rating             INT             CHECK (rating BETWEEN 1 AND 5),
    stock_count        INT             CHECK (stock_count >= 0),
    is_in_stock        BIT,
    scraped_at         DATETIME2       DEFAULT CURRENT_TIMESTAMP
);
GO


/* =========================
   Sales - Orders
========================= */
IF OBJECT_ID('sales.orders', 'U') IS NOT NULL
    DROP TABLE sales.orders;
GO

CREATE TABLE sales.orders (
    order_id           INT             PRIMARY KEY,
    customer_id        INT             NOT NULL,
    order_date         DATETIME2       NOT NULL,
    status             NVARCHAR(50)    NOT NULL CHECK (
                                        status IN ('pending', 'shipped', 'delivered', 'cancelled')
                                     ),
    payment_method     NVARCHAR(50),
    created_at         DATETIME2       DEFAULT CURRENT_TIMESTAMP
);
GO


/* =========================
   Sales - Order Items
========================= */
IF OBJECT_ID('sales.order_items', 'U') IS NOT NULL
    DROP TABLE sales.order_items;
GO

CREATE TABLE sales.order_items (
    order_item_id      INT IDENTITY(1,1) PRIMARY KEY,
    order_id           INT             NOT NULL,
    product_id         NVARCHAR(50)    NOT NULL,
    quantity           INT             NOT NULL CHECK (quantity > 0),
    unit_price         DECIMAL(10,2)   NOT NULL CHECK (unit_price >= 0),
    created_at         DATETIME2       DEFAULT CURRENT_TIMESTAMP
);
GO

