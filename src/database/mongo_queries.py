import json
from datetime import datetime
from pymongo import MongoClient

def generate_validation_report(collection, output_file="validation_report.json"):
    """
    Runs an audit on the collection and saves the results to a JSON file.
    """
    # 1. Gather Metrics
    report = {
        "timestamp": datetime.now().isoformat(),
        "total_documents": collection.count_documents({}),
        "missing_price": collection.count_documents({"price.excl_tax": None}),
        "invalid_stock": collection.count_documents({"availability.stock_count": {"$lt": 0}}),
        "top_rated_under_20": collection.count_documents({
            "rating": 5,
            "price.excl_tax": {"$lt": 20.0}
        }),
        "status": "HEALTHY" # You can add logic to flag 'WARNING' if missing_price > 0
    }

    # 2. Logic to flag Data Quality warnings
    if report["missing_price"] > 0 or report["invalid_stock"] > 0:
        report["status"] = "DATA_QUALITY_WARNING"

    # 3. Save to File
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=4)
    
    print(f"📊 Validation Report generated: {output_file}")
    return report

if __name__ == "__main__":
    URI = "mongodb://localhost:27017/"
    DB_NAME = "bookstore_inventory"
    COLLECTION_NAME = "products"

    client = MongoClient(URI)
    collection = client[DB_NAME][COLLECTION_NAME]

    # Generate and save the report
    report_data = generate_validation_report(collection, output_file=f"data/reports/validation_report.json")
    
    # Optional: Quick console summary
    print(f"Total: {report_data['total_documents']} | Status: {report_data['status']}")