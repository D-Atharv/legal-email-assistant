"""
Pydantic model for the structured JSON output of analyze_email().

Matches assignment-required schema:
{
    intent: str,
    primary_topic: str,
    parties: { client, counterparty },
    agreement_reference: { type, date },
    questions: [...],
    requested_due_date: str | null,
    urgency_level: str
}

Ensures consistent shape before drafting.
"""


from typing import List, Optional
from pydantic import BaseModel, Field


class PartiesModel(BaseModel):
    client: Optional[str] = Field(default=None)
    counterparty: Optional[str] = Field(default=None)


class AgreementReferenceModel(BaseModel):
    type: Optional[str] = Field(default=None)
    date: Optional[str] = Field(default=None)


class AnalysisSchema(BaseModel):
    intent: str
    primary_topic: str

    parties: PartiesModel
    agreement_reference: AgreementReferenceModel

    questions: List[str] = Field(default_factory=list)

    requested_due_date: Optional[str] = Field(default=None)
    urgency_level: str

    class Config:
        extra = "ignore"
