"""
Service wrapper around the deterministic draft generator.

Loads required clauses, calls generate_draft_reply(),
and returns the final drafted email.
"""

from modules.drafter import generate_draft_reply
from modules.contract_store import ContractStore

async def draft_reply_service(email_text: str, analysis: dict, contract_text: str):
    store = ContractStore(contract_text)
    clauses = store.get_all_clauses()
    draft = generate_draft_reply(
        analysis=analysis,
        clauses=clauses,
        original_email=email_text
    )
    return draft
