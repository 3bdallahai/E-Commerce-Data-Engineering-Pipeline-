import pyodbc
from pymongo import MongoClient


# =========================
# CONFIGURATION
# =========================
SQL_SERVER = '.'
DATABASE = 'ecommerce_db'

MONGO_URI = "mongodb://localhost:27017/"
MONGO_DB = "bookstore_inventory"


# =========================
# CONNECTION FUNCTIONS
# =========================
def get_sql_connection():
    conn_str = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        f"SERVER={SQL_SERVER};"
        f"DATABASE={DATABASE};"
        "Trusted_Connection=yes;"
    )
    return pyodbc.connect(conn_str)


def get_mongo_collection(collection_name):
    client = MongoClient(MONGO_URI)
    db = client[MONGO_DB]
    return db[collection_name]


# =========================
# EXTRACT
# =========================
def extract_products():
    collection = get_mongo_collection("products")
    return list(collection.find({}))


# =========================
# TRANSFORM
# =========================
def transform_products(docs):
    transformed = []

    for p in docs:
        try:
            # Safe extraction for nested fields
            availability = p.get('availability', {})
            price_info = p.get('price', {})

            stock_count = availability.get('stock_count', 0)
            is_in_stock = 1 if availability.get('is_in_stock', False) else 0
            price = price_info.get('excl_tax', 0)

            record = (
                str(p.get('_id')),
                p.get('title'),
                p.get('category'),
                p.get('rating'),
                stock_count,
                is_in_stock,
                price
            )

            # Basic validation
            if record[1] is None:
                continue  # skip if title missing

            transformed.append(record)

        except Exception as e:
            print(f"Skipping product due to error: {e}")

    return transformed


# =========================
# LOAD
# =========================
def load_products(data):
    conn = get_sql_connection()
    cursor = conn.cursor()

    insert_sql = """
        INSERT INTO inventory.products (
            product_id, title, category, rating,
            stock_count, is_in_stock, price
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """

    try:
        cursor.fast_executemany = True
        cursor.executemany(insert_sql, data)
        conn.commit()
        print(f"{len(data)} products inserted successfully.")

    except Exception as e:
        print(f"Load error: {e}")
        conn.rollback()

    finally:
        conn.close()


# =========================
# VALIDATION
# =========================
def validate_load():
    conn = get_sql_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT TOP 5 * FROM inventory.products")
    rows = cursor.fetchall()

    print("\nSample Data:")
    for row in rows:
        print(row)

    conn.close()


# =========================
# MAIN PIPELINE
# =========================
def run_pipeline():
    print("Starting Products ETL...")

    raw_data = extract_products()
    print(f"Extracted {len(raw_data)} records")

    transformed_data = transform_products(raw_data)
    print(f"Transformed {len(transformed_data)} records")

    load_products(transformed_data)

    validate_load()

    print("Products ETL Completed ✅")


if __name__ == "__main__":
    run_pipeline()