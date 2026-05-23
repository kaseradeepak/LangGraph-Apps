# Problem Statement

# Build a customer support system with:

# A classifier node
# Billing agent
# Technical agent
# General agent
# Quality checker
# Final response

# Supervisor / Coordinator Multi-Agent Architecture

from typing import Literal
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END

class SupportState(TypedDict, total=False):
    query: str
    category: Literal["billing", "technical", "general"]
    answer: str
    quality_score: int

def classify_query(state: SupportState) -> SupportState:
    """
    Supervisor-like node.
    It decides which specialist agent should handle the query.
    """
    query = state["query"].lower()

    if "refund" in query or "payment" in query or "invoice" in query:
        category = "billing"
    elif "error" in query or "bug" in query or "not working" in query:
        category = "technical"
    else:
        category = "general"

    return {"category": category}

def route_to_agent(state: SupportState) -> str:
    """
    Routing function used by conditional edges.
    """
    return state["category"]

def billing_agent(state: SupportState) -> SupportState:
    return {
        "answer": (
            "Billing Agent: I checked your payment/refund related issue. "
            "Please share your order ID so we can verify the transaction."
        )
    }

def technical_agent(state: SupportState) -> SupportState:
    return {
        "answer": (
            "Technical Agent: This looks like a technical issue. "
            "Please try clearing cache and restarting the app. "
            "If the issue continues, share the error screenshot."
        )
    }

def general_agent(state: SupportState) -> SupportState:
    return {
        "answer": (
            "General Agent: Thanks for reaching out. "
            "I can help you with orders, refunds, product details, or account-related queries."
        )
    }

def quality_checker(state: SupportState) -> SupportState:
    """
    Reviewer node.
    Checks if the answer is useful enough.
    """
    answer = state.get("answer", "")

    if len(answer) > 40:
        score = 9
    elif len(answer) > 30:
        score = 7
    elif len(answer) > 20:
        score = 6
    elif len(answer) > 10:
        score = 5
    else:
        score = 4

    return {"quality_score": score}

def final_response(state: SupportState) -> SupportState:
    return {
        "answer": f"{state['answer']}\n\nQuality Score: {state['quality_score']}/10"
    }

# Builder
builder = StateGraph(SupportState)

# add nodes to the Builder
builder.add_node("classify_query", classify_query)
builder.add_node("billing_agent", billing_agent)
builder.add_node("technical_agent", technical_agent)
builder.add_node("general_agent", general_agent)
builder.add_node("quality_checker", quality_checker)
builder.add_node("final_response", final_response)

# add edges to the Builder
builder.add_edge(START, "classify_query")

# Which next node will be triggered depends upon the classify_query functionality.
# if state["category"] == 'billing':
#     call billing_agent
# elif state["category"] == 'technical':
#     call technical_agent
builder.add_conditional_edges(
    "classify_query",
    route_to_agent,
    {
        "billing" : "billing_agent",
        "technical" : "technical_agent",
        "general" : "general_agent"
    }
)

builder.add_edge("billing_agent", "quality_checker")
builder.add_edge("technical_agent", "quality_checker")
builder.add_edge("general_agent", "quality_checker")

builder.add_edge("quality_checker", "final_response")
builder.add_edge("final_response", END)

graph = builder.compile()

result = graph.invoke({
    "query": "I am facing some bug while ordering from website."
})

print(result)




















