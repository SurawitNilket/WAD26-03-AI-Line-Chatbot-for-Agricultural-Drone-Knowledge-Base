from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class QueryRequest(BaseModel):
    user_id: Optional[str] = Field("test_user", description="Identifier of the user")
    question: str = Field(..., description="User's query in Thai or English")
    stream: bool = Field(False, description="Whether to stream response")

class SourceCitation(BaseModel):
    title: str
    source_name: str
    url: Optional[str] = None
    page: Optional[int] = None
    relevance_score: Optional[float] = None

class QueryResponse(BaseModel):
    question: str
    answer: str
    is_rule_based: bool
    sources: List[SourceCitation] = []
    latency_ms: float

class FeedbackRequest(BaseModel):
    user_id: str
    query: str
    score: int = Field(..., ge=1, le=5, description="Satisfaction score 1 to 5")
    comment: Optional[str] = None

class FeedbackResponse(BaseModel):
    status: str
    message: str

class RichMenuSetupResponse(BaseModel):
    status: str
    rich_menu_id: Optional[str] = None
    message: str
