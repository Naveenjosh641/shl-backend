from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd
from database import generate_embeddings

class AssessmentRecommender:
    def _init_(self, data_path='assessments_with_embeddings.pkl'):
        self.df = pd.read_pickle(data_path)
        self.embeddings = np.vstack(self.df['embedding'].values)
        
    def recommend(self, query, max_results=10, filters=None):
        query_embedding = generate_embeddings([query])[0]
        similarities = cosine_similarity([query_embedding], self.embeddings)[0]
        
        results_df = self.df.copy()
        results_df['similarity'] = similarities
        
        if filters:
            if 'max_duration' in filters:
                results_df['duration'] = pd.to_numeric(results_df['duration'], errors='coerce')
                results_df = results_df[results_df['duration'] <= filters['max_duration']]
            if 'remote_only' in filters and filters['remote_only']:
                results_df = results_df[results_df['remote_support'] == 'Yes']
            if 'adaptive_only' in filters and filters['adaptive_only']:
                results_df = results_df[results_df['adaptive_support'] == 'Yes']
        
        results_df = results_df.sort_values('similarity', ascending=False)
        return results_df.head(max_results).to_dict(orient="records")
