from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from recommendation_engine import AssessmentRecommender
import uvicorn
from recommendation_engine import AssessmentRecommender
# not from database import generate_embeddings

app = FastAPI()

class RecommendationRequest(BaseModel):
    query: str
    max_results: Optional[int] = 10
    max_duration: Optional[int] = None
    remote_only: Optional[bool] = False
    adaptive_only: Optional[bool] = False

@app.post("/recommend")
async def get_recommendations(request: RecommendationRequest):
    try:
        recommender = AssessmentRecommender()
        
        filters = {
            'max_duration': request.max_duration,
            'remote_only': request.remote_only,
            'adaptive_only': request.adaptive_only
        }
        
        recommendations = recommender.recommend(
            request.query,
            max_results=request.max_results,
            filters=filters
        )
        
        # Convert to JSON-friendly format
        results = recommendations.drop(columns=['embedding']).to_dict('records')
        return {"recommendations": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
