from fastapi import APIRouter
from app.api.v1.webhook import router as webhook_router
from app.api.v1.query import router as query_router
from app.api.v1.richmenu import router as richmenu_router
from app.api.v1.feedback import router as feedback_router

api_v1_router = APIRouter(prefix="/api/v1")
api_v1_router.include_router(webhook_router, tags=["LINE Webhook"])
api_v1_router.include_router(query_router, tags=["RAG & Query"])
api_v1_router.include_router(richmenu_router, tags=["Rich Menu"])
api_v1_router.include_router(feedback_router, tags=["Feedback"])
