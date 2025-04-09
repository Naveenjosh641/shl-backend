import csv
import re
from typing import List, Dict

def load_assessments():
    with open('shl_assessments.csv', mode='r') as file:
        return list(csv.DictReader(file))

def search_assessments(query: str) -> List[Dict]:
    if not query:
        return []
    
    assessments = load_assessments()
    query_words = set(re.findall(r'\w+', query.lower()))
    
    results = []
    for assessment in assessments:
        search_text = f"{assessment['name']} {assessment.get('keywords', '')}".lower()
        assessment_words = set(re.findall(r'\w+', search_text))
        
        match_score = len(query_words.intersection(assessment_words))
        
        if match_score > 0:
            results.append({
                'name': assessment['name'],
                'url': assessment['url'],
                'remote_support': assessment['remote_support'],
                'adaptive_support': assessment['adaptive_support'],
                'duration': assessment['duration'],
                'test_type': assessment['test_type'],
                'score': match_score
            })
    
    results.sort(key=lambda x: x['score'], reverse=True)
    return results[:10]
