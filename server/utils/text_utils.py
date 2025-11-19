"""
text_utils.py

Utility functions for:
    - Text cleaning
    - Whitespace normalization
    - Sentence trimming
    - Email-safe normalization

Used By:
    - parser.py
    - analyzer.py
    - drafter.py
"""

import re


# ============================================================
# BASIC TEXT CLEANING
# ============================================================

def clean_text(text: str | None) -> str:
    """
    Normalize whitespace, remove repeated blank lines,
    trim edges, replace weird Unicode spacing.

    Ensures clean deterministic output for:
        - parser
        - draft templates
        - LLM prompts

    Args:
        text (str): raw input text

    Returns:
        cleaned text (str)
    """
    if not text:
        return ""

    # Normalize unicode spaces
    txt = text.replace("\xa0", " ")

    # Collapse repeated blank lines
    txt = re.sub(r"\n\s*\n\s*\n+", "\n\n", txt)

    # Convert Windows CRLF → LF
    txt = txt.replace("\r\n", "\n").replace("\r", "\n")

    # Remove trailing spaces per line
    txt = "\n".join(line.rstrip() for line in txt.splitlines())

    return txt.strip()


# ============================================================
# SENTENCE UTILS
# ============================================================

def collapse_spaces(text: str) -> str:
    """
    Collapse multiple spaces into single.
    Useful when processing lines extracted via regex.
    """
    return re.sub(r"\s+", " ", text or "").strip()


def extract_sentences(text: str) -> list[str]:
    """
    Basic sentence extraction using punctuation.
    This is not NLP-level splitting—suitable only for prototypes.
    """
    if not text:
        return []

    # Split at . ! ?
    chunks = re.split(r"[.!?]\s+", text)
    sentences = [c.strip() for c in chunks if c.strip()]
    return sentences
