import csv
import re
from typing import List, Dict
import os

def load_assessments():
    """Load assessments from CSV file with error handling"""
    try:
        csv_path = os.path.join(os.path.dirname(__file__), "shl_assignments.csv")
        with open(csv_path, mode='r') as file:
            return list(csv.DictReader(file))
    except FileNotFoundError:
        raise Exception("SHL assessments CSV file not found. Please ensure shl_assignments.csv exists in the project root.")
    except Exception as e:
        raise Exception(f"Error loading assessments: {str(e)}")

def search_assessments(query: str) -> List[Dict]:
    """Search assessments using regex matching against CSV data"""
    if not query:
        return []
    
    try:
        assessments = load_assessments()
        query_words = set(re.findall(r'\w+', query.lower()))
        
        results = []
        for assessment in assessments:
            # Combine relevant fields for matching
            search_text = f"{assessment['name']} {assessment.get('keywords', '')}".lower()
            assessment_words = set(re.findall(r'\w+', search_text))
            
            # Calculate match score
            match_score = len(query_words.intersection(assessment_words))
            
            if match_score > 0:
                results.append({
                    'Assessment': f"[{assessment['name']}]({assessment['url']})",
                    'Duration': f"{assessment.get('duration', 'N/A')} minutes",
                    'Test Type': assessment.get('test_type', 'N/A'),
                    'Remote Testing': 'Yes' if str(assessment.get('remote_testing', '')).lower() == 'true' else 'No',
                    'Adaptive/IRT': 'Yes' if str(assessment.get('adaptive_irt', '')).lower() == 'true' else 'No',
                    '_score': match_score  # Internal field for sorting
                })
        
        # Sort by match score and return top 10 (excluding internal _score from final output)
        results.sort(key=lambda x: x['_score'], reverse=True)
        return [{k: v for k, v in item.items() if k != '_score'} for item in results[:10]]
    except Exception as e:
        print(f"Search error: {e}")
        return []
