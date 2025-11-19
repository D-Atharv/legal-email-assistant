"""
LangGraph workflow for the Legal Email Assistant.

This graph defines a 2-step pipeline:
1. analyze_node  → Extract structured JSON from the raw email
2. draft_node    → Generate a draft legal reply using clauses + analysis

The graph orchestrates the full workflow end-to-end without MCP.
"""

from langgraph.graph import StateGraph, END
from typing import Dict, Any
from modules.analyzer import analyze_email
from modules.drafter import generate_draft_reply
from modules.contract_store import ContractStore


# Graph State ----------------------------
class EmailState(Dict):
    email_text: str
    contract_text: str | None
    analysis: Dict[str, Any] | None
    draft: str | None


# Node 1: Analysis -----------------------
def analyze_node(state: EmailState):
    analysis = analyze_email(state["email_text"])
    return {
        "analysis": analysis
    }


# Node 2: Drafting -----------------------
def draft_node(state: EmailState):
    store = ContractStore(state["contract_text"])
    clauses = store.get_all_clauses()
    draft = generate_draft_reply(
        analysis=state["analysis"],
        clauses=clauses,
        original_email=state["email_text"]
    )
    return {"draft": draft}


# Build Graph ----------------------------
def build_email_graph():
    graph = StateGraph(EmailState)

    graph.add_node("analyze", analyze_node)
    graph.add_node("draft", draft_node)

    graph.set_entry_point("analyze")
    graph.add_edge("analyze", "draft")
    graph.add_edge("draft", END)

    return graph.compile()
