import openai
from sentence_transformers import SentenceTransformer
import numpy as np
import pandas as pd

# Load assessments data
assessments_df = pd.read_csv('shl_assessments.csv')

# Prepare descriptions
assessment_descriptions = assessments_df.apply(
    lambda row: f"{row['name']}. Test type: {row['test_type']}. Duration: {row['duration']}. Remote: {row['remote_support']}. Adaptive: {row['adaptive_support']}",
    axis=1
).tolist()

def generate_embeddings(texts):
    try:
        # Try using OpenAI embeddings first
        response = openai.Embedding.create(
            input=texts,
            model="text-embedding-ada-002"
        )
        return [item['embedding'] for item in response['data']]
    except Exception as e:
        print("⚠️ Falling back to local embedding model due to error:", e)
        # Now load and use the local model
        embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        return embedding_model.encode(texts).tolist()

# Generate embeddings
embeddings = generate_embeddings(assessment_descriptions)
assessments_df['embedding'] = embeddings

# Save for later use
assessments_df.to_pickle('assessments_with_embeddings.pkl')
