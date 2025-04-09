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
                    'name': assessment['name'],
                    'url': assessment['url'],
                    'remote_testing': assessment['remote_testing'],
                    'adaptive_irt': assessment['adaptive_irt'],
                    'duration': assessment['duration'],
                    'test_type': assessment['test_type'],
                    'score': match_score
                })
        
        # Sort by match score and return top 10
        results.sort(key=lambda x: x['score'], reverse=True)
        return results[:10]
    except Exception as e:
        print(f"Search error: {e}")
        return []
