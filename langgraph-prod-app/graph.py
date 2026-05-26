from langgraph.graph import START, END, StateGraph
from state import SupportState
from nodes import classify_message, retrieve_policy, draft_response, escalate_to_human, route_after_classification

builder = StateGraph(SupportState)

builder.add_node("classify_message", classify_message)
builder.add_node("retrieve_policy", retrieve_policy)
builder.add_node("draft_response", draft_response)
builder.add_node("escalate_to_human", escalate_to_human)

builder.add_edge(START, "classify_message")

builder.add_conditional_edges(
    "classify_message",
    route_after_classification,
    {
        "escalate": "escalate_to_human",
        "answer": "retrieve_policy",
    },
)

builder.add_edge("retrieve_policy", "draft_response")
builder.add_edge("draft_response", END)
builder.add_edge("escalate_to_human", END)

graph = builder.compile()




