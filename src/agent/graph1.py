import asyncio
import numpy as np
from typing import TypedDict, List
from langgraph.graph import StateGraph, START, END

# --- 1. The State ---
class AgentState(TypedDict):
    query: str
    sub_tasks: List[str]
    results: List[dict] 
    history: List[str] = [] 

# --- 2. The Nodes ---

async def sub_task_generator(state: AgentState):
    print("--- Generating Sub-Tasks ---")
    # Simulates breaking a query into 3 parallel chunks
    tasks = [f"part_{i}" for i in range(3)]
    
    # Simulating embedding vectors generation for the 3 chunks
    query_vecs = np.random.rand(512, 3)

    return [
        {"task_id": tasks[i], "query_vec": query_vecs[i]} 
        for i in range(3)
    ]

async def similarity_search_node(state: AgentState):
    """
    Simulates a vector similarity search.
    BUG 3 (Performance): This is a triple-nested loop. Must be vectorized.
    """
    task_id = state["sub_tasks"].pop() # BUG 4: State mutation in-place!
    
    # Large mock vector space (1000 vectors of 512 dims)
    vectors = [np.random.rand(512) for _ in range(1000)]
    query_vec = np.random.rand(512)
    
    scores = []
    # This is the performance bottleneck
    for v in vectors:
        score = 0
        for i in range(len(v)):
            score += v[i] * query_vec[i]
        scores.append(score)
    
    # Log to history
    state["history"].append(f"Computed {task_id}") 
    return {"results": [{"id": task_id, "top_score": max(scores)}]}

async def aggregator_node(state: AgentState):
    print("--- Aggregating Results ---")
    return {"query": "processed"}

# --- 3. The Graph Construction ---

builder = StateGraph(AgentState)
builder.add_node("generator", sub_task_generator)
builder.add_node("search", similarity_search_node)
builder.add_node("aggregator", aggregator_node)

builder.add_edge(START, "generator")

builder.add_edge("generator", "search")
builder.add_edge("search", "aggregator")
builder.add_edge("aggregator", END)

graph = builder.compile()

# --- 4. Execution ---
async def main():
    initial_state = {"query": "Find AI research", "results": [], "sub_tasks": []}
    
    print("Run 1...")
    await graph.ainvoke(initial_state)
    
    print("\nRun 2...")
    final_state = await graph.ainvoke(initial_state)
    print(f"Final History Length: {len(final_state['history'])}") 

if __name__ == "__main__":
    asyncio.run(main())