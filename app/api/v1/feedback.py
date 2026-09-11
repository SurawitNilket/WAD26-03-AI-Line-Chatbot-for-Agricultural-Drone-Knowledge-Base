"""
User Feedback and Satisfaction Survey Endpoint.
Satisfies Proposal Metric #3: "Collect satisfaction survey results (scores 1-5) from users."
"""
from fastapi import APIRouter
from app.models.schemas import FeedbackRequest, FeedbackResponse

router = APIRouter()

# In-memory storage for survey feedback
FEEDBACK_LOGS = []

@router.post("/feedback", response_model=FeedbackResponse)
async def submit_feedback(req: FeedbackRequest):
    FEEDBACK_LOGS.append(req.model_dump())
    print(f"[Feedback] User {req.user_id} rated: {req.score} stars for '{req.query}'")
    return FeedbackResponse(
        status="success",
        message="Thank you! Your feedback has been recorded."
    )

@router.get("/feedback/stats")
async def get_feedback_stats():
    """Returns statistics of collected user satisfaction scores."""
    if not FEEDBACK_LOGS:
        return {"total_responses": 0, "average_score": 0.0}
    scores = [item["score"] for item in FEEDBACK_LOGS]
    avg = sum(scores) / len(scores)
    return {
        "total_responses": len(FEEDBACK_LOGS),
        "average_score": round(avg, 2),
        "ratings_distribution": {
            star: scores.count(star) for star in range(1, 6)
        }
    }
