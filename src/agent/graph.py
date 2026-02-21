import asyncio
from typing import TypedDict
from langgraph.graph import StateGraph, END

# --- 1. STATE ---
class ResearchState(TypedDict):
    topic: str
    results: list[str] 

# --- 2. ASYNC NODES ---
async def web_researcher(state: ResearchState):
    print("Starting Web Research...")
    await asyncio.sleep(1) # Simulate network latency
    return {"results": ["Web: LangGraph supports async natively."]}

def news_researcher(state: ResearchState):
    print("Starting News Research...")
    # Simulated sync delay (This would block the whole event loop!)
    import time
    time.sleep(1) 
    return {"results": ["News: New version of LangGraph released today."]}

async def final_compiler(state: ResearchState):
    print("Compiling Report...")
    combined = "\n".join(state["results"])
    return {"results": [f"FINAL REPORT:\n{combined}"]}

# --- 3. GRAPH CONSTRUCTION ---
builder = StateGraph(ResearchState)

builder.add_node("web_research", web_researcher)
builder.add_node("news_research", news_researcher)
builder.add_node("compiler", final_compiler)

builder.set_entry_point("web_research")

# Web and News run in parallel
builder.add_edge("web_research", "news_research")
builder.add_edge("news_research", "compiler")
builder.add_edge("compiler", END)

graph = builder.compile()
graph.get_graph().print_ascii()

# --- 4. EXECUTION Test code ---
async def main():
    inputs = {"topic": "AI Agents"}
    # and handle the output properly.
    print("Running graph...")
    result = graph.invoke(inputs) 
    print(result)

# Logic to run the script
if __name__ == "__main__":
    main()