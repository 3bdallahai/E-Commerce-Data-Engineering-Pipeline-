from pymongo import MongoClient
import pyodbc
from collections import Counter

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
# MAIN
# =========================
order_item_data = []
missing_products = 0

try:
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    print("SQL Connection Successful!")

    # =========================
    # LOAD PRODUCT LOOKUP FROM SQL
    # =========================
    cursor.execute("SELECT product_id, title, price FROM inventory.products")

    product_map = {
        title: {
            'product_id': product_id,
            'unit_price': price
        }
        for product_id, title, price in cursor.fetchall()
    }

    print(f"Loaded {len(product_map)} products from SQL")

    # =========================
    # BUILD ORDER ITEMS
    # =========================
    for o in orders.find({}):
        order_id = o['_id']
        product_list = o.get('books', [])

        counts = Counter(product_list)

        for product, qty in counts.items():
            p_info = product_map.get(product)

            if not p_info:
                missing_products += 1
                print(f"Missing product: {product}")
                continue

            record = (
                order_id,
                p_info['product_id'],
                qty,
                p_info['unit_price']
            )

            order_item_data.append(record)

    print(f"Prepared {len(order_item_data)} order items")
    print(f"Missing products skipped: {missing_products}")

    # =========================
    # INSERT
    # =========================
    sql = """
        INSERT INTO sales.order_items (
            order_id, product_id, quantity, unit_price
        )
        VALUES (?, ?, ?, ?)
    """

    cursor.fast_executemany = True
    cursor.executemany(sql, order_item_data)

    conn.commit()

    print("Data inserted successfully ✅")

except Exception as e:
    print(f"Error: {e}")
    conn.rollback()

finally:
    cursor.close()
    conn.close()