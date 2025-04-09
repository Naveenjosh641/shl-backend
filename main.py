from fastapi import FastAPI, HTTPException, Request
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
@app.post("/recommend")  # Add POST support
async def recommend_assessments(query: str, request: Request = None):
    if not query:
        # Try to get query from POST body if not in params
        if request and request.method == "POST":
            try:
                body = await request.json()
                query = body.get("query", "")
            except:
                pass
    
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)
