import requests
from bs4 import BeautifulSoup


def get_product_links(num_pages=2):
    """
    Scrape product URLs from listing pages.

    Args:
        num_pages (int): Number of pages to scrape

    Returns:
        list: List of relative product URLs
    """
    base_url = "https://books.toscrape.com/catalogue/page-{}.html"
    product_urls = []

    for page_number in range(1, num_pages + 1):
        url = base_url.format(page_number)
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        products = soup.find_all(
            "li",
            class_="col-xs-6 col-sm-4 col-md-3 col-lg-3"
        )

        for product in products:
            link_tag = product.find("a")
            product_urls.append(link_tag["href"])

    return product_urls