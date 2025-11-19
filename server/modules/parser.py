"""
PURE LLM EMAIL PARSER (Assignment-Compliant)
Extracts clean structural components without regex logic.
"""

import json
import textwrap
from google import genai
from core.config import settings
from utils.text_utils import clean_text

client = genai.Client(api_key=settings.GEMINI_API_KEY)


def parse_email(email_text: str) -> dict:
    """
    Extract subject, greeting, body, signature, sender_name, sender_role, questions
    using ONLY LLM reasoning.
    Works on forwarded chains and irregular formats.
    """

    email_text = clean_text(email_text)

    prompt = textwrap.dedent(f"""
    You are a precise email-structure extraction engine.

    Parse the email BELOW into its structural parts.
    Return ONLY valid JSON in this schema:

    {{
      "subject": string | null,
      "greeting": string | null,
      "body": string,
      "signature_text": string | null,
      "sender_name": string | null,
      "sender_role": string | null,
      "questions": [string]
    }}

    RULES:
    • ALWAYS treat the *latest actual sender* as the sender (e.g., for forwarded chains, this is usually the person who wrote the first non-forward line).
    • Body = text between greeting and signature (if no greeting, take everything before signature).
    • Signature = name + role block at end (if any).
    • Extract ALL questions (numbered, unnumbered, bullet, or embedded “whether…” questions).
    • Do NOT hallucinate. If a field is truly missing, use null.

    EMAIL TO PARSE:
    {email_text}
    """)

    response = client.models.generate_content(
        model=settings.GEMINI_MODEL,
        contents=[prompt]
    )

    raw = response.text.strip()

    # Extract JSON strictly
    try:
        start = raw.index("{")
        end = raw.rindex("}") + 1
        parsed = json.loads(raw[start:end])
    except:
        return {
            "subject": None,
            "greeting": None,
            "body": email_text,
            "signature_text": None,
            "sender_name": None,
            "sender_role": None,
            "questions": []
        }

    parsed["body"] = clean_text(parsed.get("body", ""))
    return parsed
