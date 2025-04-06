import openai
from sentence_transformers import SentenceTransformer
import numpy as np
import pandas as pd

# Initialize embedding model (using SentenceTransformer as fallback)
try:
    embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
except:
    print("Using local embedding model")

def generate_embeddings(texts):
    try:
        # Try using OpenAI embeddings first
        response = openai.Embedding.create(
            input=texts,
            model="text-embedding-ada-002"
        )
        return [item['embedding'] for item in response['data']]
    except:
        # Fallback to local model
        return embedding_model.encode(texts).tolist()

# Load assessments data
assessments_df = pd.read_csv('shl_assessments.csv')

# Generate embeddings for each assessment
assessment_descriptions = assessments_df.apply(
    lambda row: f"{row['name']}. Test type: {row['test_type']}. Duration: {row['duration']}. Remote: {row['remote_support']}. Adaptive: {row['adaptive_support']}",
    axis=1
).tolist()

embeddings = generate_embeddings(assessment_descriptions)
assessments_df['embedding'] = embeddings

# Save embeddings for later use
assessments_df.to_pickle('assessments_with_embeddings.pkl')
