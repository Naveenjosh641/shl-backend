import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin
from your_gemini_embedding_module import generate_embedding  # Assume you built this

def scrape_shl_assessments(base_url="https://www.shl.com/solutions/products/product-catalog/"):
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    assessments = []
    
    for card in soup.select('.assessment-card'):
        name = card.select_one('.card-title').text.strip()
        relative_url = card.select_one('a')['href']
        url = urljoin(base_url, relative_url)
        
        detail_response = requests.get(url)
        detail_soup = BeautifulSoup(detail_response.text, 'html.parser')
        
        remote_support = "Yes" if "remote" in detail_soup.text.lower() else "No"
        adaptive_support = "Yes" if "adaptive" in detail_soup.text.lower() else "No"
        
        duration = detail_soup.select_one('.duration').text.strip() if detail_soup.select_one('.duration') else "N/A"
        test_type = detail_soup.select_one('.test-type').text.strip() if detail_soup.select_one('.test-type') else "N/A"
        
        # Combine text for embedding
        text_for_embedding = f"{name}. {test_type}. Duration: {duration}. Remote: {remote_support}. Adaptive: {adaptive_support}"
        
        # Generate Gemini embedding (you need to implement this function)
        embedding = generate_embedding(text_for_embedding)
        
        assessments.append({
            "name": name,
            "url": url,
            "remote_support": remote_support,
            "adaptive_support": adaptive_support,
            "duration": duration,
            "test_type": test_type,
            "embedding": embedding
        })
    
    return pd.DataFrame(assessments)

df = scrape_shl_assessments()

# Save with embedding (you might want to save separately using pickle/parquet depending on size)
df.to_pickle("shl_assessments_with_embeddings.pkl")
