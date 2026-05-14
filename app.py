from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END

# Define the state of the application
# TypedDict defines the structure of StateGraph.
class SupportedState(TypedDict):
    user_query: str
    category: str
    answer: str

# Node-1
# user_query = When will I get My Refund?
def classify_query(state: SupportedState):
    query = state["user_query"].lower()

    if "refund" in query:
        category = "refund"
    elif "return" in query or "returns" in query:
        category = "return"
    elif "shipping" in query or "delivery" in query or "delivered" in query:
        category = "delivery"
    else:
        category = "general"
    
    return {"category" : category}

# Node-2
def answer_query(state: SupportedState):
    category = state["category"]
    query = state["user_query"]

    # Here, we should call the LLM with RAG to answer the user query based on the company's knowledge base.
    answer = ""
    if category == "return":
        answer = "You can return the product with in 7 days of delivery"
    elif category == "refund":
        answer = "Refund will be processed with in 5-7 working days."
    elif category == "delivery":
        answer = "Orders are generally delivered with 3-5 days."
    else:
        category = "For any other general query, please call our customer care."

    return {"answer" : answer}

# Build the Graph.
builder = StateGraph(SupportedState)

# add nodes.
builder.add_node("classify_query", classify_query)
builder.add_node("answer_query", answer_query)

# add edges.
builder.add_edge(START, "classify_query")
builder.add_edge("classify_query", "answer_query")
builder.add_edge("answer_query", END)

graph = builder.compile()

# Run the graph.
result = graph.invoke(
    {
        "user_query" : "When my order will be delivered",
        "category" : "",
        "answer" : ""
    }
)

print(result)





    

