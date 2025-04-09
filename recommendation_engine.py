from database import search_assessments
from typing import List, Dict

class AssessmentRecommender:
    def recommend_assessments(self, query: str) -> List[Dict]:
        return search_assessments(query)
