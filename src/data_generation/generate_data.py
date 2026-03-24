from faker import Faker
import json
import random
from src.storage.data_lake import save_to_jsonl


def get_book_titles(file_path="data/raw/books.jsonl"):
    """
    Load book titles from the data lake.

    Args:
        file_path (str): Path to books JSONL file

    Returns:
        list: List of book titles
    """
    titles = []

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            data = json.loads(line)
            titles.append(data.get("title"))

    print(f"Number of books found: {len(titles)}")
    return titles


def create_customers(fake, num_customers=10):
    """
    Generate synthetic customer data.

    Args:
        fake (Faker): Faker instance
        num_customers (int): Number of customers

    Returns:
        list: List of customer dictionaries
    """
    customers = []

    for i in range(num_customers):
        customer_id = 1250000 + i

        customer = {
            "customer_id": customer_id,
            "name": fake.name(),
            "address": fake.address(),
            "email": fake.email(),
            "date_of_birth": fake.date_of_birth().isoformat(),
            "phone_number": fake.phone_number()
        }

        customers.append(customer)

    print(f"Customers created: {len(customers)}")
    return customers


def create_orders(fake, customers, books, num_orders=20):
    """
    Generate synthetic order data.

    Args:
        fake (Faker): Faker instance
        customers (list): List of customer records
        books (list): List of book titles
        num_orders (int): Number of orders

    Returns:
        list: List of order dictionaries
    """
    orders = []

    customer_ids = [c["customer_id"] for c in customers]

    for i in range(num_orders):
        order = {
            "order_id": 5120000 + i,

            # Ensure valid relationship with customers
            "customer_id": random.choice(customer_ids),

            # Each order contains 1–3 books
            "books": random.sample(books, k=random.randint(1, 3)),

            # FIX: choices → choice
            "status": random.choice(
                ["processing", "shipped", "cancelled", "delivered"]
            ),

            "order_date": fake.date_between(start_date="-3y").isoformat(),

            "payment_method": random.choice(
                ["card", "cash", "apple_pay"]
            )
        }

        orders.append(order)

    print(f"Orders created: {len(orders)}")
    return orders


def save_records(file_path, records):
    """
    Save multiple records to JSONL file.

    Args:
        file_path (str): Output file path
        records (list): List of dictionaries
    """
    for record in records:
        save_to_jsonl(file_path, record)


if __name__ == "__main__":
    Faker.seed(15)
    fake = Faker()

    # Load existing book data
    books = get_book_titles()

    # Generate synthetic data
    customers = create_customers(fake, num_customers=1274)
    orders = create_orders(fake, customers, books, num_orders=5531)

    # Save to data lake
    save_records("data/raw/customers.jsonl", customers)
    save_records("data/raw/orders.jsonl", orders)