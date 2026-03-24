import json
from datetime import datetime
from pymongo import MongoClient


def generate_validation_report(db, output_file="data/reports/validation_report.json"):
    """
    Generate validation report across products, customers, and orders.
    """

    products = db["products"]
    customers = db["customers"]
    orders = db["orders"]

    report = {
        "timestamp": datetime.now().isoformat(),

        # ---------------- PRODUCTS ----------------
        "products": {
            "total": products.count_documents({}),
            "missing_price": products.count_documents({"price.excl_tax": None}),
            "invalid_stock": products.count_documents({"availability.stock_count": {"$lt": 0}})
        },

        # ---------------- CUSTOMERS ----------------
        "customers": {
            "total": customers.count_documents({}),
            "missing_email": customers.count_documents({"email": None})
        },

        # ---------------- ORDERS ----------------
        "orders": {
            "total": orders.count_documents({}),
            "missing_customer": orders.count_documents({"customer_id": None}),
            "invalid_status": orders.count_documents({
                "status": {"$nin": ["processing", "shipped", "cancelled", "delivered"]}
            })
        }
    }

    # 🔥 RELATIONSHIP CHECK (IMPORTANT)
    valid_customer_ids = set(c["_id"] for c in customers.find({}, {"_id": 1}))

    invalid_orders = 0
    for order in orders.find({}, {"customer_id": 1}):
        if order["customer_id"] not in valid_customer_ids:
            invalid_orders += 1

    report["orders"]["invalid_customer_reference"] = invalid_orders

    # Global status
    report["status"] = "HEALTHY"
    if (
        report["products"]["missing_price"] > 0
        or report["orders"]["invalid_customer_reference"] > 0
    ):
        report["status"] = "DATA_QUALITY_WARNING"

    # Save report
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4)

    print(f"📊 Validation report saved to {output_file}")
    return report


if __name__ == "__main__":
    URI = "mongodb://localhost:27017/"
    DB_NAME = "bookstore_inventory"

    client = MongoClient(URI)
    db = client[DB_NAME]

    report = generate_validation_report(db)

    print(f"Status: {report['status']}")