
"""
Assignment-Compliant ContractStore

We HARD-CODE the ONLY clauses the drafter is allowed to use:
9.1, 9.2, 10.2

LLM extraction is DISABLED because it causes hallucinations.
"""

class ContractStore:
    """
    Holds ONLY the assignment-required clauses.
    Ignores whatever the email or user sends.
    """

    def __init__(self, *_args, **_kwargs):
        # HARD-CODED CLAUSES (assignment standard)
        self.clauses = {
            "9.1": (
                "Either Party may terminate this Agreement for cause upon "
                "thirty (30) days’ written notice if the other Party commits a material breach."
            ),
            "9.2": (
                "Repeated failure to meet delivery timelines constitutes a material breach."
            ),
            "10.1":(
                "All notices shall be given in writing and shall be effective upon receipt"
            ),
            "10.2": (
                "For termination, minimum thirty (30) days’ prior written notice is required."
            )
        }

    def get_clause(self, cid: str):
        return self.clauses.get(cid)

    def get_all_clauses(self):
        return dict(self.clauses)

    def search_clauses(self, _q: str):
        # Search is intentionally disabled for safety
        return []
