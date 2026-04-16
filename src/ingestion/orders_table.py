from pymongo import MongoClient
import pyodbc

# =========================
# CONFIG
# =========================
server = '.'
database = 'ecommerce_db'

conn_str = (
    f'DRIVER={{ODBC Driver 17 for SQL Server}};'
    f'SERVER={server};'
    f'DATABASE={database};'
    'Trusted_Connection=yes;'
)

URI = "mongodb://localhost:27017/"
DB_NAME = "bookstore_inventory"


# =========================
# CONNECTIONS
# =========================
client = MongoClient(URI)
db = client[DB_NAME]
orders = db["orders"]


# =========================
# TRANSFORM FUNCTION
# =========================
def transform_orders(mongo_orders):
    orders_data = []

    for o in mongo_orders:
        # Normalize status
        status = 'pending' if o.get('status') == 'processing' else o.get('status')

        record = (
            o['_id'],
            o['customer_id'],
            o['order_date'],
            status,
            o.get('payment_method')
        )

        orders_data.append(record)

    return orders_data


# =========================
# LOAD FUNCTION
# =========================
def load_orders(cursor, orders_data):
    sql = """
        INSERT INTO sales.orders (
            order_id, customer_id, order_date, status, payment_method
        )
        VALUES (?, ?, ?, ?, ?)
    """

    cursor.fast_executemany = True
    cursor.executemany(sql, orders_data)


# =========================
# MAIN
# =========================
try:
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    print("SQL Connection Successful!")

    # Extract
    mongo_orders = list(orders.find({}))
    print(f"Extracted {len(mongo_orders)} orders from MongoDB")

    # Transform
    orders_data = transform_orders(mongo_orders)
    print(f"Transformed {len(orders_data)} orders")

    # Load
    load_orders(cursor, orders_data)
    conn.commit()

    print("Orders loaded successfully ✅")

except Exception as e:
    print(f"Error: {e}")
    conn.rollback()

finally:
    cursor.close()
    conn.close()