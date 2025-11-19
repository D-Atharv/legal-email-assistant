"""
FastAPI Route: POST /draft

Inputs:
- raw email text
- analysis JSON from /analyze
- contract snippet

Returns:
- fully drafted legal reply email
"""


from fastapi import APIRouter, HTTPException
from models.request_models import DraftRequest
from services.drafting_service import draft_reply_service

router = APIRouter()


@router.post("/", summary="Draft legal reply", description="Draft the reply email using JSON analysis + contract snippet.")
async def draft_email_endpoint(payload: DraftRequest):
    """
    POST /draft
    Body:
        {
            "email_text": "...",
            "analysis": { ... JSON ... },
            "contract_text": "Clause 9.1 ... Clause 9.2 ..."
        }
    Response:
        {
            "draft": "Dear Ms. Sharma,..."
        }
    """
    try:
        draft_text = await draft_reply_service(
            email_text=payload.email_text,
            analysis=payload.analysis,
            contract_text=payload.contract_text
        )
        return {"draft": draft_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
