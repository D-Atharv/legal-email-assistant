"""
PURE LLM ANALYZER (No Regex, No Heuristics)

This module uses a single strong Gemini call to extract all required fields:
- intent
- primary_topic
- parties (client, counterparty)
- agreement_reference (type, date)
- questions
- requested_due_date
- urgency_level

Regex is NOT used anywhere.
All reasoning is left to the LLM.
Output is validated using AnalysisSchema.
"""

import json
from typing import Dict, Any

from google import genai
from core.config import settings
from models.analysis_schema import AnalysisSchema
from utils.text_utils import clean_text


# ---------------------------------------------------------
# LLM CLIENT
# ---------------------------------------------------------
client = genai.Client(api_key=settings.GEMINI_API_KEY)


# ---------------------------------------------------------
# MAIN ANALYSIS FUNCTION
# ---------------------------------------------------------

def analyze_email(email_text: str) -> Dict[str, Any]:
    """
    PURE LLM version of analyze_email():
    - Sends the ENTIRE email to Gemini
    - Asks it to extract ALL fields
    - Forces strict JSON output
    - Validates with AnalysisSchema
    """

    email_text = clean_text(email_text)

    prompt = f"""
You are a legal email analysis engine.

Extract structured information from the email below.
Return ONLY valid JSON EXACTLY in this schema:

{{
  "intent": "string",
  "primary_topic": "string",

  "parties": {{
    "client": "string or null",
    "counterparty": "string or null"
  }},

  "agreement_reference": {{
    "type": "string or null",
    "date": "ISO date string (YYYY-MM-DD) or null"
  }},

  "questions": ["list of legal questions"],

  "requested_due_date": "ISO date string or null",

  "urgency_level": "low | medium | high"
}}

RULES:
- Convert all dates to ISO format (YYYY-MM-DD).
- Extract client and counterparty names ONLY (no nicknames, no quotes).
- Extract ALL legal questions, including:
  * bullet points
  * “whether” statements
  * implicit questions
  * multi-line questions
- If urgency is implied by phrases like:
    "tomorrow", "end of day", "ASAP", "before noon", 
    treat urgency as high.
- Do NOT hallucinate. If unsure, use null.
- Output ONLY JSON. No explanations.

Email:
{email_text}
"""

    response = client.models.generate_content(
        model=settings.GEMINI_MODEL,
        contents=prompt
    )

    raw = response.text.strip()

    # Ensure JSON extraction
    try:
        data = json.loads(raw)
    except:
        # Try to locate JSON inside any surrounding text
        try:
            start = raw.index("{")
            end = raw.rindex("}") + 1
            data = json.loads(raw[start:end])
        except:
            raise ValueError("LLM did not return valid JSON:\n" + raw)

    # Validate with Pydantic
    validated = AnalysisSchema(**data)
    return validated.model_dump()
