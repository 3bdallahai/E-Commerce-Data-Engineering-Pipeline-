# 📊 E-commerce Data Engineering Pipeline

## 🚀 Project Overview

This project demonstrates the design and implementation of a **data engineering pipeline** for an e-commerce use case.
The pipeline ingests product data from a website, stores it in a data lake, processes it, and loads it into a database for querying and analysis.

The goal is to simulate a **real-world data pipeline architecture** using modern data engineering practices.

---

## 🏗️ Architecture

```
Web Scraping → JSONL Data Lake → MongoDB (Staging Layer) → Validation Reports
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

---

## 📂 Project Structure

```
ecommerce-data-pipeline/
│
├── data/
│   ├── raw/              # JSONL data lake
│   └── reports/          # Validation reports
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
│   └── storage/
│       └── data_lake.py
│
├── main.py               # Pipeline orchestration
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

---

## 🧠 Key Concepts Demonstrated

* Data Lake design using JSONL
* Batch processing & memory-efficient ingestion
* Idempotent pipelines using upserts
* Schema design in NoSQL databases
* Indexing for query optimization
* Data quality validation and reporting
* Modular pipeline architecture

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

---

## 🚧 Next Steps

* Load data into a relational database (MySQL)
* Design normalized or star schema
* Build analytics layer
* Add dashboard for visualization

---


## ⭐ Notes

This project is designed as a **portfolio project** to demonstrate practical data engineering skills, including pipeline design, data ingestion, transformation, and validation.

---
