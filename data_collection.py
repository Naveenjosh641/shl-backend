import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin

def scrape_shl_assessments(base_url="https://www.shl.com/solutions/products/product-catalog/"):
    # Fetch the main catalog page
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    assessments = []
    
    # Find all assessment cards (adjust selector based on actual page structure)
    for card in soup.select('.assessment-card'):
        name = card.select_one('.card-title').text.strip()
        relative_url = card.select_one('a')['href']
        url = urljoin(base_url, relative_url)
        
        # Fetch detailed information from individual assessment pages
        detail_response = requests.get(url)
        detail_soup = BeautifulSoup(detail_response.text, 'html.parser')
        
        # Extract additional attributes (these selectors need to be adjusted)
        remote_support = "Yes" if "remote" in detail_soup.text.lower() else "No"
        adaptive_support = "Yes" if "adaptive" in detail_soup.text.lower() else "No"
        
        duration = detail_soup.select_one('.duration').text.strip() if detail_soup.select_one('.duration') else "N/A"
        test_type = detail_soup.select_one('.test-type').text.strip() if detail_soup.select_one('.test-type') else "N/A"
        
        assessments.append({
            "name": name,
            "url": url,
            "remote_support": remote_support,
            "adaptive_support": adaptive_support,
            "duration": duration,
            "test_type": test_type
        })
    
    return pd.DataFrame(assessments)

# Save to CSV for later use
assessments_df = scrape_shl_assessments()
assessments_df.to_csv('shl_assessments.csv', index=False)
