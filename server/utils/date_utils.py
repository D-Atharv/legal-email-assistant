"""
date_utils.py

Provides:
    - Robust date parsing from loose natural-language formats
    - Safe ISO-8601 standardization
    - Urgency calculation based on due date
        * high   -> <= 2 days from today
        * medium -> <= 7 days
        * low    -> otherwise

Used By:
    - analyzer.py
    - MCP tool: tool_compute_urgency_level
"""

from datetime import datetime, timedelta
from dateutil import parser as date_parse


# ============================================================
# SAFE DATE PARSING
# ============================================================

def parse_date_safe(date_str: str | None) -> str | None:
    """
    Safely parse dates like:
        - 10 March 2023
        - March 10, 2023
        - 1 December 2025
        - 18 Nov 2025
    Convert to ISO format: YYYY-MM-DD

    Returns None if unparseable.
    """
    if not date_str or not date_str.strip():
        return None

    try:
        dt = date_parse.parse(date_str, dayfirst=True)
        return dt.date().isoformat()  # YYYY-MM-DD
    except Exception:
        return None


# ============================================================
# URGENCY CALCULATION
# ============================================================

def compute_urgency(due_date_iso: str | None) -> str:
    """
    Determine urgency based on due date relative to TODAY (UTC).

    Rules (assignment requirement):
        - HIGH urgency:   due within 2 days
        - MEDIUM urgency: due within 7 days
        - LOW urgency:    later or no date provided

    Args:
        due_date_iso (str): ISO format "YYYY-MM-DD"

    Returns:
        "high" | "medium" | "low"
    """
    if not due_date_iso:
        return "low"

    try:
        due_dt = datetime.fromisoformat(due_date_iso)
    except Exception:
        return "low"

    today = datetime.utcnow()
    delta = (due_dt - today).days

    if delta <= 2:
        return "high"
    if delta <= 7:
        return "medium"
    return "low"
