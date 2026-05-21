from typing import TypedDict
from langgraph.graph import StateGraph, END

from agents import agent_alpha, agent_beta

class FactCheckState(TypedDict):
    claim: str
    evidence: str
    verification_status: str
    decision: str

def build_graph():
    workflow = StateGraph(FactCheckState)

    workflow.add_node("investigator", agent_alpha)
    workflow.add_node("archivist", agent_beta)

    workflow.set_entry_point("investigator")

    workflow.add_edge("investigator", "archivist")
    workflow.add_edge("archivist", END)

    return workflow.compile()


graph = build_graph()