import sqlite3
from typing import List, Dict
import re

class Database:
    def __init__(self, db_path: str = "shl_assessments.db"):
        self.conn = sqlite3.connect(db_path)
        self.create_tables()
    
    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS assessments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                url TEXT,
                remote_testing TEXT,
                adaptive_irt TEXT,
                duration TEXT,
                test_type TEXT,
                keywords TEXT
            )
        ''')
        self.conn.commit()
    
    def insert_assessment(self, assessment: Dict):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO assessments (name, url, remote_testing, adaptive_irt, duration, test_type, keywords)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            assessment['name'],
            assessment['url'],
            assessment['remote_testing'],
            assessment['adaptive_irt'],
            assessment['duration'],
            assessment['test_type'],
            assessment.get('keywords', '')
        ))
        self.conn.commit()
    
    def search_assessments(self, query: str, limit: int = 10) -> List[Dict]:
        cursor = self.conn.cursor()
        
        # Process query and find matches
        query_keywords = set(re.findall(r'\w+', query.lower()))
        
        cursor.execute('SELECT * FROM assessments')
        all_assessments = cursor.fetchall()
        
        # Score assessments based on keyword matches
        scored_assessments = []
        for assessment in all_assessments:
            id_, name, url, remote, adaptive, duration, test_type, keywords = assessment
            assessment_keywords = set(re.findall(r'\w+', (name + ' ' + keywords).lower()))
            match_score = len(query_keywords.intersection(assessment_keywords))
            
            scored_assessments.append({
                'score': match_score,
                'name': name,
                'url': url,
                'remote_testing': remote,
                'adaptive_irt': adaptive,
                'duration': duration,
                'test_type': test_type
            })
        
        # Sort by match score and return top results
        scored_assessments.sort(key=lambda x: x['score'], reverse=True)
        return [item for item in scored_assessments if item['score'] > 0][:limit]
    
    def close(self):
        self.conn.close()
