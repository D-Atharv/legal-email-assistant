"""
Request models for FastAPI routes:

- AnalyzeRequest → POST /analyze
- DraftRequest   → POST /draft

These models validate user input and guarantee that the service
layer receives correct parameter structures.
"""
from typing import Dict, Any

from pydantic import BaseModel, Field


# ============================================================
# Request Model: /analyze
# ============================================================

class AnalyzeRequest(BaseModel):
    email_text: str = Field(
        ...,
        description="Raw legal email text that must be analyzed."
    )
    # contract_text is optional for analysis (Part 1 only)
    contract_text: str | None = Field(
        default=None,
        description="Optional contract snippet text (not required for analysis)."
    )


# ============================================================
# Request Model: /draft
# ============================================================

class DraftRequest(BaseModel):
    email_text: str = Field(
        ...,
        description="Original raw email text used to detect sender name."
    )

    analysis: Dict[str, Any] = Field(
        ...,
        description="JSON output from analyze_email()."
    )

    contract_text: str = Field(
        ...,
        description="Contract snippet containing clauses (9.1, 9.2, 10.2)."
    )
