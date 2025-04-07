def evaluate_recommendations(test_queries, ground_truth, recommender, k=3):
    recall_scores = []
    ap_scores = []
    
    for query, relevant_assessments in zip(test_queries, ground_truth):
        recommendations = recommender.recommend(query, max_results=k)
        recommended_names = set(recommendations['name'].tolist())
        relevant_set = set(relevant_assessments)
        
        # Calculate Recall@K
        intersection = recommended_names & relevant_set
        recall = len(intersection) / len(relevant_set) if relevant_set else 0
        recall_scores.append(recall)
        
        # Calculate AP@K
        ap = 0.0
        num_relevant = 0
        for i, name in enumerate(recommendations['name'], 1):
            if name in relevant_set:
                num_relevant += 1
                precision_at_i = num_relevant / i
                ap += precision_at_i
        
        ap = ap / min(k, len(relevant_set)) if relevant_set else 0
        ap_scores.append(ap)
    
    mean_recall = sum(recall_scores) / len(recall_scores)
    mean_ap = sum(ap_scores) / len(ap_scores)
    
    return {
        "mean_recall@k": mean_recall,
        "map@k": mean_ap,
        "recall_scores": recall_scores,
        "ap_scores": ap_scores
    }
