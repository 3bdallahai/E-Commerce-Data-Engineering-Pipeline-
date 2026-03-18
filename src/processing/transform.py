import re
from datetime import datetime

# Helper: convert rating text → number
RATING_MAP = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}

BASE_URL = "http://books.toscrape.com/"


def parse_price(price_str):
    if not price_str:
        return None
    return float(price_str.replace("£", "").strip())


def parse_stock(availability_str):
    if not availability_str:
        return False, 0
    
    is_in_stock = "In stock" in availability_str
    
    match = re.search(r"\((\d+) available\)", availability_str)
    stock_count = int(match.group(1)) if match else 0
    
    return is_in_stock, stock_count


def clean_image_url(url):
    if url.startswith("../../"):
        return BASE_URL + url.replace("../../", "")
    return url


def parse_date(date_str):
    # Example: '24th Jun 2016 09:29'
    try:
        return datetime.strptime(
            re.sub(r"(st|nd|rd|th)", "", date_str),
            "%d %b %Y %H:%M"
        )
    except:
        return None


def transform_book(raw):
    """
    Transform raw scraped book data into a semi-structured format
    suitable for MongoDB storage.

    Args:
        raw (dict): Raw scraped book data

    Returns:
        dict: Cleaned and structured document
    """
    is_in_stock, stock_count = parse_stock(raw.get("Availability"))

    cleaned = {
        "title": raw.get("title"),
        "category": raw.get("category"),
        "product_type": raw.get("Product Type"),
        "upc": raw.get("UPC"),

        "description": raw.get("description"),

        "price": {
            "excl_tax": parse_price(raw.get("Price (excl. tax)")),
            "incl_tax": parse_price(raw.get("Price (incl. tax)")),
            "tax": parse_price(raw.get("Tax")),
            "currency": "GBP"
        },

        "availability": {
            "is_in_stock": is_in_stock,
            "stock_count": stock_count,
            "raw": raw.get("Availability")
        },

        "rating": RATING_MAP.get(raw.get("rating"), None),
        "num_reviews": int(raw.get("Number of reviews", 0)),

        "image_url": clean_image_url(raw.get("image_link", "")),

        "book_uploaded_date": parse_date(raw.get("book_uploaded_date")),
        "scraped_at": raw.get("scraped_at")
    }

    return cleaned