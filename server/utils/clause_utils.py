"""
clause_utils.py

Helper utilities for:
    - Clause substring search
    - Light fuzzy matching for fallback
    - Pretty formatting for clause excerpts

Used By:
    - contract_store.py
    - analyzer_service (optional)
    - mcp_tools.py
"""

from typing import Dict, List, Tuple


# ============================================================
# SUBSTRING SEARCH
# ============================================================

def search_clauses_substring(clauses: Dict[str, str], query: str) -> List[Tuple[str, str]]:
    """
    Simple case-insensitive substring search through all clause texts.

    Args:
        clauses (dict): { "9.1": "text", "9.2": "text", ... }
        query (str): search string

    Returns:
        list[ (clause_id, clause_text) ]
    """
    if not query:
        return []

    query = query.lower()

    matches = []
    for cid, text in clauses.items():
        if query in text.lower():
            matches.append((cid, text))

    return matches


# ============================================================
# LIGHT FUZZY MATCHING (very simple)
# ============================================================

def fuzzy_match_clauses(clauses: Dict[str, str], query: str) -> List[Tuple[str, float]]:
    """
    Minimal fuzzy matcher (ratio of matching words).
    This is intentionally lightweight for prototype — we do NOT depend on heavy libraries.

    Args:
        clauses: dict of clause_id -> clause text
        query: string to match semantically

    Returns:
        list of (clause_id, score) sorted by score desc
    """
    if not query:
        return []

    query_words = set(query.lower().split())
    results = []

    for cid, text in clauses.items():
        text_words = set(text.lower().split())

        # Score = fraction of overlap (very naive)
        overlap = query_words & text_words
        score = len(overlap) / max(len(query_words), 1)

        if score > 0:  # only keep some overlap
            results.append((cid, score))

    # Sort by score descending
    results.sort(key=lambda x: x[1], reverse=True)
    return results


# ============================================================
# FORMATTING HELPERS
# ============================================================

def format_clause_excerpts(clauses: Dict[str, str], limit: int = 200) -> str:
    """
    Produce a human-readable block of clause excerpts,
    each limited to `limit` characters.

    Returns:
        string formatted:
            Clause 9.1: <excerpt>
            Clause 9.2: <excerpt>
            ...
    """
    lines = []
    for cid, text in clauses.items():
        excerpt = text.strip()
        if len(excerpt) > limit:
            excerpt = excerpt[: limit - 3].rstrip() + "..."
        lines.append(f"Clause {cid}: {excerpt}")

    return "\n".join(lines)
