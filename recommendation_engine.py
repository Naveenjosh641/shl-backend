from database import Database
from typing import List, Dict

class AssessmentRecommender:
    def __init__(self):
        self.db = Database()
    
    def recommend_assessments(self, query: str) -> List[Dict]:
        """
        Recommends assessments based on the input query
        Args:
            query: Natural language query or job description
        Returns:
            List of recommended assessments with their details
        """
        # Search assessments using the keyword-based approach
        assessments = self.db.search_assessments(query)
        
        # Format the results
        recommendations = []
        for assessment in assessments:
            recommendations.append({
                'name': assessment['name'],
                'url': assessment['url'],
                'remote_testing': assessment['remote_testing'],
                'adaptive_irt': assessment['adaptive_irt'],
                'duration': assessment['duration'],
                'test_type': assessment['test_type']
            })
        
        return recommendations
    
    def close(self):
        self.db.close()
