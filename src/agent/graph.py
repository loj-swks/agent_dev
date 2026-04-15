import asyncio
from typing import TypedDict
from langgraph.graph import StateGraph, END, START

# --- 1. STATE ---
class ProcessState(TypedDict):
    changeme: str

def dummy_node(state: ProcessState) -> ProcessState:
    # Simulate some processing
    return {}

# --- 3. GRAPH CONSTRUCTION ---
builder = StateGraph(ProcessState)
builder.add_node("dummy_node", dummy_node)

builder.add_edge(START, "dummy_node")  # Connect start state to the dummy node
builder.add_edge("dummy_node", END)  # Connect to end state

graph = builder.compile()
graph.get_graph().print_ascii()
