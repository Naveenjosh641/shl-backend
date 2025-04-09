from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from recommendation_engine import AssessmentRecommender

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

recommender = AssessmentRecommender()

@app.get("/recommend")
async def recommend_assessments(query: str):
    if not query:
        raise HTTPException(status_code=400, detail="Query parameter is required")
    
    try:
        recommendations = recommender.recommend_assessments(query)
        return {
            "status": "success",
            "results": recommendations
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Corrected the main block
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)
