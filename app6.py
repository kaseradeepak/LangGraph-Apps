# Streaming & Real-Time Updates.
# Without streaming, the user sees nothing until the graph finishes.

# Streaming Modes 

# 1. updates - Shows the udpates after each node.
# 2. messages - Streams the LLM tokens.
# 3. custom - customize output

# Problem Statement

# Build a research workflow that streams progress while running.

# Search documents
# Analyze documents
# Generate answer

import time
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.config import get_stream_writer

class ResearchState(TypedDict, total=False):
    topic: str
    documents: list[str]
    analysis: str
    final_answer: str

def search_documents(state: ResearchState) -> ResearchState:
    writer = get_stream_writer()

    writer("Searching documents...")
    time.sleep(2) # delay of 10 sec

    docs = [
        f"Document 1 about {state['topic']}",
        f"Document 2 about {state['topic']}",
    ]

    writer(f"Found {len(docs)} documents.")

    return {"documents": docs}

def analyze_documents(state: ResearchState) -> ResearchState:
    writer = get_stream_writer()

    writer("Analyzing documents...")
    time.sleep(2) # delay of 2 sec

    analysis = f"Key insights extracted from {len(state['documents'])} documents."

    writer("Analysis completed.")

    return {"analysis": analysis}

def generate_answer(state: ResearchState) -> ResearchState:
    writer = get_stream_writer()

    writer("Generating final answer...")
    time.sleep(2)

    answer = f"Final answer for topic '{state['topic']}': {state['analysis']}"

    writer("Final answer ready.")

    return {"final_answer": answer}

builder = StateGraph(ResearchState)

builder.add_node("search_documents", search_documents)
builder.add_node("analyze_documents", analyze_documents)
builder.add_node("generate_answer", generate_answer)

builder.add_edge(START, "search_documents")
builder.add_edge("search_documents", "analyze_documents")
builder.add_edge("analyze_documents", "generate_answer")
builder.add_edge("generate_answer", END)

graph = builder.compile()

for chunk in graph.stream(
    {"topic": "LangGraph for AI agents"},
    stream_mode=["updates"],
    version="v2",
):
        print("STATE UPDATE:", chunk["data"])

# result = graph.invoke(
#     {"topic" : "LangGraph for AI agents"}
# )

# print(result)

# Monitoring & Observability 
#




