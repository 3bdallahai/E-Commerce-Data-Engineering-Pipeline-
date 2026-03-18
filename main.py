from src.scraping.product_links import get_product_links
from src.scraping.product_details import scrape_product_details
from src.processing.transform import transform_book
from src.storage.data_lake import save_to_jsonl


def run_pipeline():
    """
    Main pipeline:
    - Get product links
    - Scrape product details
    - Transform data
    - Save to data lake (JSONL)
    """
    product_links = get_product_links(num_pages=50)

    for link in product_links:
        try:
            raw_data = scrape_product_details(link)
            cleaned_data = transform_book(raw_data)

            save_to_jsonl("data/raw/books.jsonl", cleaned_data)

        except Exception as e:
            print(f"Error processing {link}: {e}")


if __name__ == "__main__":
    run_pipeline()