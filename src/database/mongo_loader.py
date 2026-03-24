import json
from datetime import datetime
from pymongo import MongoClient, UpdateOne
from pymongo.errors import BulkWriteError


def get_collection(uri, db_name, collection_name):
    """Create MongoDB connection and return collection."""
    client = MongoClient(uri)
    return client[db_name][collection_name]


# -----------------------------
# DATASET CONFIGURATION
# -----------------------------
DATASET_CONFIG = {
    "products": {
        "id_field": "upc",
        "date_fields": ["scraped_at", "book_uploaded_date"],
        "required_fields": ["upc", "title", "price"],
        "indexes": [
            "price.excl_tax",
            "rating",
            "availability.is_in_stock"
        ]
    },
    "customers": {
        "id_field": "customer_id",
        "date_fields": ["date_of_birth"],
        "required_fields": ["customer_id", "email"],
        "indexes": ["email"]
    },
    "orders": {
        "id_field": "order_id",
        "date_fields": ["order_date"],
        "required_fields": ["order_id", "customer_id"],
        "indexes": ["customer_id", "order_date", "status"]
    }
}


def parse_dates(data, date_fields):
    """Convert ISO string fields into datetime objects."""
    for field in date_fields:
        if field in data and isinstance(data[field], str):
            try:
                data[field] = datetime.fromisoformat(data[field])
            except Exception:
                pass
    return data


def validate_document(data, required_fields):
    """Validate required fields exist."""
    for field in required_fields:
        if field not in data or data[field] is None:
            return False
    return True


def create_indexes(collection, index_fields):
    """Create indexes dynamically."""
    for field in index_fields:
        collection.create_index(field)


def load_dataset(file_path, collection, dataset_type, batch_size=500):
    """
    Generic loader for any dataset (products, customers, orders).
    """
    config = DATASET_CONFIG[dataset_type]

    id_field = config["id_field"]
    date_fields = config["date_fields"]
    required_fields = config["required_fields"]

    operations = []
    total_processed = 0

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            try:
                data = json.loads(line)

                # Validate
                if not validate_document(data, required_fields):
                    continue

                # Parse dates
                data = parse_dates(data, date_fields)

                # Assign _id dynamically
                data["_id"] = data.pop(id_field)

                # Prepare upsert
                operations.append(
                    UpdateOne(
                        {"_id": data["_id"]},
                        {"$set": data},
                        upsert=True
                    )
                )

                # Batch execution
                if len(operations) >= batch_size:
                    execute_batch(collection, operations)
                    total_processed += len(operations)
                    operations = []

            except Exception as e:
                print(f"Skipping record: {e}")

    # Remaining batch
    if operations:
        execute_batch(collection, operations)
        total_processed += len(operations)

    print(f"{dataset_type.upper()} → Total processed: {total_processed}")


def execute_batch(collection, operations):
    """Execute bulk write safely."""
    try:
        result = collection.bulk_write(operations)
        print(f"Matched: {result.matched_count}, Upserted: {result.upserted_count}")
    except BulkWriteError as bwe:
        print(f"Bulk write error: {bwe.details}")


# -----------------------------
# MAIN
# -----------------------------
if __name__ == "__main__":
    URI = "mongodb://localhost:27017/"
    DB_NAME = "bookstore_inventory"

    datasets = [
        ("products", "data/raw/books.jsonl"),
        ("customers", "data/raw/customers.jsonl"),
        ("orders", "data/raw/orders.jsonl"),
    ]

    for dataset_name, file_path in datasets:
        print(f"\n🔄 Loading {dataset_name}...")

        collection = get_collection(URI, DB_NAME, dataset_name)

        create_indexes(
            collection,
            DATASET_CONFIG[dataset_name]["indexes"]
        )

        load_dataset(file_path, collection, dataset_name)