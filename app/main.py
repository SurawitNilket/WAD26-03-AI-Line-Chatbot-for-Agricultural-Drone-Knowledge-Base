"""
Main FastAPI Application Entry Point.
Course: 2026 EN813701 Web Application Development
Project: AI LINE Chatbot for Agricultural Drone Knowledge Base
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api.v1 import api_v1_router

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=(
        "Backend API for AI LINE Agricultural Drone Chatbot. "
        "Provides LINE Webhook handling, RAG retrieval with cited DOAE/CAAT references, "
        "rule-based fast answers, and Rich Menu management."
    ),
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS for external dashboard or testing tools
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API Routers
app.include_router(api_v1_router)

@app.get("/")
async def root():
    return {
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "online",
        "docs": "/docs",
        "endpoints": {
            "webhook": "/api/v1/webhook",
            "query": "/api/v1/query",
            "richmenu_config": "/api/v1/richmenu/config",
            "richmenu_setup": "/api/v1/richmenu/setup",
            "feedback": "/api/v1/feedback",
            "health": "/api/v1/health"
        }
    }

@app.get("/api/v1/health")
async def health_check():
    return {
        "status": "healthy",
        "llm_model": settings.LLM_MODEL,
        "environment": settings.APP_ENV,
        "has_line_token": bool(settings.LINE_CHANNEL_ACCESS_TOKEN and settings.LINE_CHANNEL_ACCESS_TOKEN != "dummy_line_channel_access_token"),
        "has_gemini_key": bool(settings.GEMINI_API_KEY)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        reload=True
    )
