import pyodbc
from pymongo import MongoClient
from datetime import datetime


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
def extract_customers():
    collection = get_mongo_collection("customers")
    return list(collection.find({}))


# =========================
# TRANSFORM
# =========================
def transform_customers(docs):
    transformed = []

    for d in docs:
        try:
            record = (
                int(d.get('_id')),
                d.get('name'),
                d.get('email'),
                d.get('date_of_birth'),
                d.get('address'),
                d.get('phone_number'),
            )

            # Basic validation
            if record[1] is None or record[2] is None:
                continue  # skip bad records

            transformed.append(record)

        except Exception as e:
            print(f"Skipping record due to error: {e}")

    return transformed


# =========================
# LOAD
# =========================
def load_customers(data):
    conn = get_sql_connection()
    cursor = conn.cursor()

    insert_sql = """
        INSERT INTO crm.customers (
            customer_id, name, email, date_of_birth, address, phone_number
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """

    try:
        cursor.fast_executemany = True
        cursor.executemany(insert_sql, data)
        conn.commit()
        print(f"{len(data)} customers inserted successfully.")

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

    cursor.execute("SELECT TOP 5 * FROM crm.customers")
    rows = cursor.fetchall()

    print("\nSample Data:")
    for row in rows:
        print(row)

    conn.close()


# =========================
# MAIN PIPELINE
# =========================
def run_pipeline():
    print("Starting Customer ETL...")

    raw_data = extract_customers()
    print(f"Extracted {len(raw_data)} records")

    transformed_data = transform_customers(raw_data)
    print(f"Transformed {len(transformed_data)} records")

    load_customers(transformed_data)

    validate_load()

    print("Customer ETL Completed ✅")


if __name__ == "__main__":
    run_pipeline()