import json
from datetime import datetime
from pymongo import MongoClient, UpdateOne
from pymongo.errors import BulkWriteError


def get_mongo_collection(uri, db_name, collection_name):
    """
    Initialize MongoDB connection and return collection.
    """
    client = MongoClient(uri)
    db = client[db_name]
    return db[collection_name]


def parse_dates(data):
    """
    Convert ISO string dates into datetime objects.
    """
    try:
        if "scraped_at" in data:
            data["scraped_at"] = datetime.fromisoformat(data["scraped_at"])

        if "book_uploaded_date" in data:
            data["book_uploaded_date"] = datetime.fromisoformat(data["book_uploaded_date"])

    except Exception as e:
        raise ValueError(f"Date parsing error: {e}")

    return data


def validate_document(data):
    """
    Basic validation to ensure required fields exist.
    """
    required_fields = ["upc", "title", "price"]

    for field in required_fields:
        if field not in data or data[field] is None:
            return False

    return True


def create_indexes(collection):
    """
    Create indexes to optimize query performance.
    Runs safely multiple times (MongoDB ignores duplicates).
    """
    collection.create_index("price.excl_tax")
    collection.create_index("rating")
    collection.create_index("availability.is_in_stock")


def load_and_upsert(file_path, collection, batch_size=500):
    """
    Load JSONL data and upsert into MongoDB in batches.

    Args:
        file_path (str): Path to JSONL file
        collection: MongoDB collection
        batch_size (int): Number of operations per batch
    """
    operations = []
    total_processed = 0

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            try:
                data = json.loads(line)

                # Validate document
                if not validate_document(data):
                    continue

                # Convert date fields
                data = parse_dates(data)

                # Use UPC as unique _id
                data["_id"] = data.pop("upc")

                # Prepare upsert operation
                operations.append(
                    UpdateOne(
                        {"_id": data["_id"]},
                        {"$set": data},
                        upsert=True
                    )
                )

                # Execute batch
                if len(operations) >= batch_size:
                    execute_batch(collection, operations)
                    total_processed += len(operations)
                    operations = []

            except Exception as e:
                print(f"Skipping invalid record: {e}")

    # Insert remaining operations
    if operations:
        execute_batch(collection, operations)
        total_processed += len(operations)

    print(f"Total processed: {total_processed}")


def execute_batch(collection, operations):
    """
    Execute bulk write safely.
    """
    try:
        result = collection.bulk_write(operations)
        print(
            f"Matched: {result.matched_count}, "
            f"Upserted: {result.upserted_count}"
        )
    except BulkWriteError as bwe:
        print(f"Bulk write error: {bwe.details}")


if __name__ == "__main__":
    # Config (can later move to config file)
    URI = "mongodb://localhost:27017/"
    DB_NAME = "bookstore_inventory"
    COLLECTION_NAME = "products"
    FILE_PATH = "data/raw/books.jsonl"

    collection = get_mongo_collection(URI, DB_NAME, COLLECTION_NAME)

    create_indexes(collection)
    load_and_upsert(FILE_PATH, collection)