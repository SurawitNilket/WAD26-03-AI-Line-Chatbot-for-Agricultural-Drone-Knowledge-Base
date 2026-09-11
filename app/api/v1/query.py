"""
Direct REST Query Endpoint.
Enables instant local and remote testing of the RAG & Rule engine
without requiring an active LINE tunnel.
"""
from fastapi import APIRouter
from app.models.schemas import QueryRequest, QueryResponse, SourceCitation
from app.core.dispatcher import dispatcher

router = APIRouter()

@router.post("/query", response_model=QueryResponse)
async def query_endpoint(req: QueryRequest):
    result = dispatcher.handle_text_message(
        user_id=req.user_id or "web_user",
        reply_token="test_token",
        text=req.question
    )

    citations = [
        SourceCitation(**c) for c in result.get("citations", [])
    ]

    return QueryResponse(
        question=req.question,
        answer=result.get("response", ""),
        is_rule_based=result.get("is_rule_based", False),
        sources=citations,
        latency_ms=result.get("latency_ms", 0.0)
    )
