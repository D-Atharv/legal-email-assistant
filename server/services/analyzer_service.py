"""
Service layer for running analyze_email().

Thin abstraction that allows:
- FastAPI routes
- LangGraph nodes
to reuse the same analysis logic.
"""

from modules.analyzer import analyze_email

async def analyze_email_service(email_text: str):
    return analyze_email(email_text)
