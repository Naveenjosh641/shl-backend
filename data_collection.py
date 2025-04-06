from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

app = FastAPI()

@app.get("/")
def root():
    return {"message": "SHL Assessment Scraper is running."}

@app.get("/scrape")
def scrape_shl_assessments():
    base_url = "https://www.shl.com/solutions/products/product-catalog/"
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    assessments = []

    for card in soup.select('.assessment-card'):
        name_tag = card.select_one('.card-title')
        link_tag = card.select_one('a')
        if not name_tag or not link_tag:
            continue

        name = name_tag.text.strip()
        url = urljoin(base_url, link_tag['href'])

        detail_response = requests.get(url)
        detail_soup = BeautifulSoup(detail_response.text, 'html.parser')

        remote_support = "Yes" if "remote" in detail_soup.text.lower() else "No"
        adaptive_support = "Yes" if "adaptive" in detail_soup.text.lower() else "No"
        duration = detail_soup.select_one('.duration')
        test_type = detail_soup.select_one('.test-type')

        assessments.append({
            "name": name,
            "url": url,
            "remote_support": remote_support,
            "adaptive_support": adaptive_support,
            "duration": duration.text.strip() if duration else "N/A",
            "test_type": test_type.text.strip() if test_type else "N/A"
        })

    return {"assessments": assessments}
