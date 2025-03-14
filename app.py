from flask import Flask, jsonify, request
from flask_cors import CORS
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing

def init_driver():
    options = Options()
    options.add_argument("--headless")  # Run headless for no UI
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def get_titles(driver, url):
    driver.get(url)
    titles = []
    try:
        title_elements = driver.find_elements(By.TAG_NAME, 'h2')
        for title in title_elements:
            titles.append(title.text)
    except Exception as e:
        print("Error getting titles:", e)
    return titles

def get_descriptions(driver, url):
    driver.get(url)
    descriptions = []
    try:
        description_elements = driver.find_elements(By.CLASS_NAME, 'description-class')  # Update the correct class name
        for description in description_elements:
            descriptions.append(description.text)
    except Exception as e:
        print("Error getting descriptions:", e)
    return descriptions

def get_images(driver, url):
    driver.get(url)
    images = []
    try:
        image_elements = driver.find_elements(By.TAG_NAME, 'img')
        for img in image_elements:
            src = img.get_attribute('src')
            if src:
                images.append(src)
    except Exception as e:
        print("Error getting images:", e)
    return images

def get_reviews(driver, url):
    driver.get(url)
    reviews = []
    try:
        review_elements = driver.find_elements(By.CLASS_NAME, 'review-class')  # Update the correct class name
        for review in review_elements:
            reviews.append(review.text)
    except Exception as e:
        print("Error getting reviews:", e)
    return reviews

@app.route('/scrape', methods=['POST'])
def scrape_data():
    data = request.json
    url = data.get('url')
    data_type = data.get('data_type')

    driver = init_driver()
    result = {}

    if data_type == 'titles':
        result['titles'] = get_titles(driver, url)
    elif data_type == 'descriptions':
        result['descriptions'] = get_descriptions(driver, url)
    elif data_type == 'images':
        result['images'] = get_images(driver, url)
    elif data_type == 'reviews':
        result['reviews'] = get_reviews(driver, url)

    driver.quit()

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
