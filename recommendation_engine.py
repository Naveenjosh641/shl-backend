from database import search_assessments
from typing import List, Dict

class AssessmentRecommender:
    def recommend_assessments(self, query: str) -> List[Dict]:
        """Get recommendations from CSV using regex"""
        try:
            return search_assessments(query)
        except Exception as e:
            print(f"Recommendation error: {e}")
            return []
