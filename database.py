import requests

API_KEY = "AIzaSyC3uUbmMcd8BuJ1ti6ejMs_81g9EhbPQiI"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

def generate_embeddings(texts):
    embeddings = []
    for text in texts:
        prompt = f"Generate a numerical vector representation (embedding) for the following text:\n\n\"{text}\""
        payload = {
            "contents": [
                {
                    "parts": [{"text": prompt}]
                }
            ]
        }
        response = requests.post(GEMINI_URL, json=payload)
        data = response.json()

        try:
            content = data['candidates'][0]['content']['parts'][0]['text']
            # Convert string of numbers to list of floats
            vector = [float(x) for x in content.strip("[]").split(",")]
            embeddings.append(vector)
        except Exception as e:
            raise ValueError(f"Failed to extract embedding: {e}\nResponse: {data}")
    
    return embeddings
