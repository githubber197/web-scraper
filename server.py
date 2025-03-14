from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

def fetch_html(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        return str(e)

def parse_data(html, data_type):
    soup = BeautifulSoup(html, 'html.parser')
    extractors = {
        "titles": lambda s: [title.get_text(strip=True) for title in s.find_all('h1')],
        "prices": lambda s: [price.get_text(strip=True) for price in s.find_all(class_='price')],
        "descriptions": lambda s: [desc.get_text(strip=True) for desc in s.find_all('p')],
        "images": lambda s: [img['src'] for img in s.find_all('img', src=True)]
    }
    return extractors.get(data_type, lambda s: [])(soup)

@app.route('/scrape', methods=['POST'])
def scrape():
    data = request.get_json()
    url = data.get("url")
    data_type = data.get("dataType")

    if not url or not data_type:
        return jsonify({"success": False, "error": "Missing URL or data type."})

    html = fetch_html(url)
    if not html:
        return jsonify({"success": False, "error": "Error fetching HTML."})

    scraped_data = parse_data(html, data_type)
    return jsonify({"success": True, "results": scraped_data})

if __name__ == '__main__':
    app.run(debug=True)
