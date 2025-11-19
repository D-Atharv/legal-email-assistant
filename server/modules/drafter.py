"""
PURE LLM DRAFTER (Assignment-Compliant)

Produces a professional legal reply that:
- Uses ONLY provided clauses
- Answers ONLY based on snippet
- Says “Based on the provided excerpt… cannot confirm” when needed
- Uses proper legal tone like the assignment example
"""

import json
from google import genai
from core.config import settings
from utils.text_utils import clean_text

client = genai.Client(api_key=settings.GEMINI_API_KEY)

def generate_draft_reply(analysis: dict, clauses: dict, original_email: str) -> str:
    """
    Fully compliant drafter.
    Uses ONLY the 3 allowed clauses.
    """

    clause_block = "\n".join([f"{cid}: {text}" for cid, text in clauses.items()])

    prompt = f"""
You are a senior commercial contracts lawyer.

Produce a reply that:
- Uses a professional legal tone.
- Addresses the sender by name.
- Answers ALL questions exactly as in the JSON.
- Uses ONLY these clauses (do not add others):
  {clause_block}
- If the clause needed to answer the question is NOT in this list,
  you MUST write:
  "Based on the provided excerpt, this clause is not included, so we cannot confirm."
- NEVER invent or infer clauses.
- NEVER reference clauses not in the hardcoded list.
- NEVER declare breach unless the snippet explicitly defines one.
- DO NOT output JSON.

ORIGINAL EMAIL:
{original_email}

STRUCTURED ANALYSIS:
{json.dumps(analysis, indent=2)}

--- DRAFT THE EMAIL BELOW THIS LINE ONLY ---
"""

    resp = client.models.generate_content(
        model=settings.GEMINI_MODEL,
        contents=[prompt]
    )

    return clean_text(resp.text)
