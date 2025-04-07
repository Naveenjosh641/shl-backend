from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd
from database import generate_embeddings

class AssessmentRecommender:
    def __init__(self, data_path='assessments_with_embeddings.pkl'):
        self.df = pd.read_pickle(data_path)
        self.embeddings = np.array(self.df['embedding'].tolist())
        
    def recommend(self, query, max_results=10, filters=None):
        # Generate query embedding
        query_embedding = generate_embeddings([query])[0]
        
        # Calculate similarities
        similarities = cosine_similarity(
            [query_embedding],
            self.embeddings
        )[0]
        
        # Add similarity scores to dataframe
        results_df = self.df.copy()
        results_df['similarity'] = similarities
        
        # Apply filters if provided
        if filters:
            if 'max_duration' in filters:
                results_df = results_df[results_df['duration'] <= filters['max_duration']]
            if 'remote_only' in filters and filters['remote_only']:
                results_df = results_df[results_df['remote_support'] == 'Yes']
            if 'adaptive_only' in filters and filters['adaptive_only']:
                results_df = results_df[results_df['adaptive_support'] == 'Yes']
        
        # Sort and return top results
        results_df = results_df.sort_values('similarity', ascending=False)
        return results_df.head(max_results)
