# 📊 E-commerce Data Engineering Pipeline

## 🚀 Project Overview

This project demonstrates the design and implementation of a **data engineering pipeline** for an e-commerce use case.
The pipeline ingests product data from a website, stores it in a data lake, processes it, and loads it into a database for querying and analysis.

The goal is to simulate a **real-world data pipeline architecture** using modern data engineering practices.

---

## 🏗️ Architecture

```
Web Scraping
      ↓
JSONL Data Lake (Raw Storage)
      ↓
MongoDB (Staging / NoSQL Layer)
      ↓
Python ETL Pipeline
      ↓
SQL Server (OLTP Relational Layer)

```

### 🔹 Layers Explained

* **Data Source**
  Scraped product data from an e-commerce website.

* **Data Lake (Raw Layer)**
  Data is stored locally in **JSON Lines (JSONL)** format to simulate a data lake.

* **Processing Layer**
  Data is semi-processed using Python:

  * Price converted to numeric format
  * Stock extracted from text
  * Ratings normalized
  * Dates parsed

* **MongoDB (Staging Layer)**
  Semi-structured data is stored in MongoDB for:

  * Efficient querying
  * Flexible schema handling
  * Intermediate validation before loading into a relational database

* **Validation Layer**
  Data quality checks are performed and saved as **validation reports**.

* **ETL Layer (Python Pipeline)**

moving data from MongoDB to SQL Server while transforming it into a structured relational format:

  * Extracting data from MongoDB collections
  * Transforming nested and semi-structured data into tabular format
  * Building relationships between entities (customers, orders, products)
  * Aggregating order-level data into order items
  * Enriching data using lookup mappings (e.g., product price and IDs)
  * Loading cleaned data into SQL Server tables


* **OLTP Layer (SQL Server) **
Structured transactional database optimized for operational use.

  * Storing normalized relational tables (customers, products, orders, order_items)
  * Enforcing data integrity using primary and foreign keys
  * Applying constraints to ensure data quality and consistency
  * Indexing key columns for performance optimization
  * Storing derived operational fields (e.g., total order amount)
---

## 📂 Project Structure

```
ecommerce-data-pipeline/
│
├── data/
│   ├── raw/              # JSONL data lake
│   └── reports/          # Validation reports
|
├── SQL/
│   ├── schemas.sql              # create tables
│   ├── constraints.sql          # add FK and constraints
│   └── post_load.sql
│
├── diagrams/
│   ├── ERD_digram.png
│   └── OLTP_DB_diagram.png
│
├── src/
│   ├── scraping/
│   │   ├── product_links.py
│   │   └── product_details.py
│   │
│   ├── processing/
│   │   └── transform.py
│   │
│   ├── database/
│   │   ├── mongo_loader.py
│   │   └── mongo_queries.py
│   │
│   ├── scraping/
│   │   ├── customers_table.py
│   │   ├── order_items_table.py
│   │   ├── order_table.py
│   │   └── products_table.py
│   │
│   └── storage/
│       └── data_lake.py
│
├── main.py               # Pipeline orchestration
│
├── requirements.txt
│
└── README.md
```

---

## ⚙️ Features Implemented

### 🔹 Web Scraping

* Extract product links from listing pages
* Scrape detailed product information from each page

### 🔹 Data Lake (JSONL)

* Store data in **JSON Lines format**
* Efficient and scalable for large datasets
* Acts as the **raw data source of truth**

### 🔹 Data Transformation

* Semi-structured data processing using Python
* Clean and normalize key fields:

  * Prices → float
  * Stock → integer
  * Ratings → numeric
  * Dates → datetime

### 🔹 MongoDB Ingestion

* Batch-based ingestion for performance
* Upsert operations to avoid duplicates
* Unique identifier using `UPC`
* Indexing for optimized queries:

  * price
  * rating
  * availability

### 🔹 Data Validation

* Validation checks include:

  * Missing values
  * Invalid stock values
  * Data consistency
* Results stored as JSON reports


### 🔹 ETL Layer (Python Pipeline)

* Extracted data from MongoDB collections (customers, products, orders)
* Built transformation logic to convert semi-structured data into relational format
* Flattened nested structures (e.g., product availability and pricing)
* Normalized inconsistent values (e.g., order status standardization)
* Created product lookup mapping for data enrichment
* Aggregated order data into order_items using frequency-based logic
* Handled missing and inconsistent data safely
* Loaded transformed data into SQL Server using batch inserts
* Optimized performance using fast_executemany


### 🔹 OLTP Layer (SQL Server)

* Designed normalized relational schema for e-commerce domain
* Implemented core tables:
    * customers
    * products
    * orders
    * order_items
* Defined primary keys and foreign key relationships
* Enforced data integrity using constraints (NOT NULL, CHECK, UNIQUE)
* Added indexing on frequently queried columns
* Introduced derived field total_amount in orders table
* Supported efficient transactional queries and joins
* Ensured referential integrity across all tables
---

## 🧠 Key Concepts Demonstrated

* Data Lake design using JSONL
* Batch processing & memory-efficient ingestion
* Idempotent pipelines using upserts
* Schema design in NoSQL databases
* Indexing for query optimization
* Data quality validation and reporting
* Modular pipeline architecture
* Multi-layer data engineering pipeline (Raw → Staging → OLTP)

---

## 📊 Example Queries

* Find top-rated affordable books
* Filter products by price range
* Check stock availability

---

## 🛠️ Technologies Used

* Python
* BeautifulSoup (Web Scraping)
* MongoDB
* JSON / JSONL
* Regex (Data Parsing)
* PyODBC

---

## 🚧 Next Steps

* Build analytics layer
* Add dashboard for visualization

---


## ⭐ Notes

This project is designed as a **portfolio project** to demonstrate practical data engineering skills, including pipeline design, data ingestion, transformation, and validation.

---
