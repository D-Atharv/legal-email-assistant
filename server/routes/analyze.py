"""
FastAPI Route: POST /analyze

Uses the analyzer_service to:
- Parse + analyze a raw legal email
- Return structured JSON defined by AnalysisSchema
"""


from fastapi import APIRouter, HTTPException
from models.request_models import AnalyzeRequest
from services.analyzer_service import analyze_email_service

router = APIRouter()


@router.post("/", summary="Analyze legal email", description="Parse and analyze a raw legal email.")
async def analyze_email_endpoint(payload: AnalyzeRequest):
    """
    POST /analyze
    Body:
        {
            "email_text": "raw email text ..."
        }
    Response:
        { JSON analysis }
    """
    try:
        result = await analyze_email_service(payload.email_text)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
