/*
=============================================================
CONSTRAINTS & INDEXES
=============================================================
Purpose:
    Adds foreign keys, unique constraints, and indexes
*/

USE ecommerce_db;
GO



/* =========================
   FOREIGN KEYS
========================= */

-- Orders → Customers
ALTER TABLE sales.orders
ADD CONSTRAINT FK_orders_customer
FOREIGN KEY (customer_id)
REFERENCES crm.customers(customer_id);
GO


-- Order Items → Orders
ALTER TABLE sales.order_items
ADD CONSTRAINT FK_order_items_order
FOREIGN KEY (order_id)
REFERENCES sales.orders(order_id);
GO


-- Order Items → Products
ALTER TABLE sales.order_items
ADD CONSTRAINT FK_order_items_product
FOREIGN KEY (product_id)
REFERENCES inventory.products(product_id);
GO


/* =========================
   INDEXES
========================= */

-- Orders
CREATE INDEX idx_orders_customer_id 
ON sales.orders(customer_id);

CREATE INDEX idx_orders_date 
ON sales.orders(order_date);


-- Order Items
CREATE INDEX idx_order_items_order_id 
ON sales.order_items(order_id);

CREATE INDEX idx_order_items_product_id 
ON sales.order_items(product_id);
GO