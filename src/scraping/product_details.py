import requests
from bs4 import BeautifulSoup
from datetime import datetime


BASE_URL = "https://books.toscrape.com/catalogue/"


def scrape_product_details(relative_url):
    """
    Extract raw product data from a product page.

    Args:
        relative_url (str): Relative product URL

    Returns:
        dict: Raw product data
    """
    url = BASE_URL + relative_url
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Metadata
    date_added = soup.find('meta', attrs={'name': 'created'})['content']

    # Image
    image_link = soup.find('div', id="product_gallery").find('img')['src']

    # Main product section
    product_main = soup.find('div', class_='product_main')

    title = product_main.find('h1').get_text()
    rating = product_main.find('p', class_='star-rating')['class'][1]

    # Description
    desc_tag = soup.find('div', id='product_description')
    description = (
        desc_tag.find_next_sibling('p').get_text()
        if desc_tag else "no description found"
    )

    # Base dictionary
    book_data = {
        "category": "Book",
        "title": title,
        "rating": rating,
        "description": description,
        "image_link": image_link,
        "book_uploaded_date": date_added,
        "scraped_at": datetime.now()
    }

    # Table data
    table = soup.find('table', class_='table-striped')
    for row in table.find_all('tr'):
        key = row.find('th').get_text(strip=True)
        value = row.find('td').get_text(strip=True)
        book_data[key] = value

    return book_data