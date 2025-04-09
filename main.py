from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from recommendation_engine import AssessmentRecommender
import uvicorn

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
        recommendations = recommender.recommend_assessments(request.query)
        return {"recommendations": recommendations}
    except Exception as e:
        print(f"Error: {e}")

if _name_ == "_main_":
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
