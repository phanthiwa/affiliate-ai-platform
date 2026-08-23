from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import router as api_router

app = FastAPI(
    title="Affiliate Growth OS - API",
    description="AI-powered Affiliate Content Automation Engine tailored for Thai Creators & Google Flow",
    version="1.0.0"
)

# Enable CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "affiliate-growth-os-backend",
        "market": "Thailand (TikTok Shop, Shopee Video, FB Reels)",
        "features": ["Product Scoring", "11-Section Intelligence", "Batch 10-15 Clips", "Google Flow Video Provider"]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
