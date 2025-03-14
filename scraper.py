import requests
from bs4 import BeautifulSoup

def fetch_html(url):
    """Fetch HTML content from a given URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

def parse_data(html, data_type):
    """Parse HTML for specific data type (e.g., titles, prices, descriptions)."""
    soup = BeautifulSoup(html, 'html.parser')
    extractors = {
        "titles": lambda s: [title.get_text(strip=True) for title in s.find_all('h1')],
        "prices": lambda s: [price.get_text(strip=True) for price in s.find_all(class_='price')],
        "descriptions": lambda s: [desc.get_text(strip=True) for desc in s.find_all('p')],
        "images": lambda s: [img['src'] for img in s.find_all('img', src=True)],
    }
    return extractors.get(data_type, lambda s: [])(soup)
