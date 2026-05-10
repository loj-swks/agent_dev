import asyncio
from pydantic import BaseModel, Field
from typing import TypedDict, List

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, END, START
from searchlib.search_engine import IssueSearchEngine, DiscussionSearchEngine



# ==== Data Models ====
class DiscussionRecord(BaseModel):
    discussion_id: str
    issue_id: str
    sender: str
    message: str
class IssueRecord(BaseModel):
    issue_id: str
    platform: str
    priority: str
    title: str
    description: str
    discussions: List[DiscussionRecord]
    assignee: str
    created_date: str
    summary: str = Field(
        default="", 
        description=(
            "Summary of the issue in the format of: "
            "Title: <title>\n"
            "Description: <description>\n"
            "Assignee: <assignee>\n"
            "Created Date: <created_date>\n"
            "Discussions: <list of discussions in the format of [sender: message]>\n"
        )
    )
          
# --- 0. INITIAL SETUP ---
issue_engine = IssueSearchEngine()
discussion_engine = DiscussionSearchEngine()

# --- 1. STATE ---
class IssueState(TypedDict):
    query_keywords: str  # search keywords string separated by space
    query_ids: str  # search issue by ids string separated by space
    results: List[IssueRecord]

# --- 2. NODES ---
def search_issues(state: IssueState):
    keywords = state['query_keywords'].split()
    for keyword in keywords:
        results = issue_engine.asearch(keyword)
    state['results'] = [IssueRecord(**issue) for issue in results]
    return state

def search_discussions(state: IssueState):
    for issue in state['results']:
        discussions = discussion_engine.asearch(issue.issue_id)
        issue.discussions = [DiscussionRecord(**disc) for disc in discussions]
    return state

def id_search_start(state: IssueState):
    return


def search_issues_by_id(state: IssueState):
    ids = state['query_ids'].split()
    results = []
    for id in ids:
        issue = issue_engine.asearch_by_id(id)
        if issue:
            results.append(issue)
    state['results'] = [IssueRecord(**issue) for issue in results]
    return state

def search_discussions_by_issue_id(state: IssueState):
    for issue in state['results']:
        discussions = discussion_engine.asearch(issue.issue_id)
        issue.discussions = [DiscussionRecord(**disc) for disc in discussions]
    return state

def route_by_input(state: IssueState):
    if state['query_keywords']:
        return ["search_issues"]
    elif state['query_ids']:
        return ["id_search_start"]
    else:
        raise ValueError("No valid input for routing")

# --- 3. GRAPH CONSTRUCTION ---
builder = StateGraph(IssueState)

builder.add_node("search_issues", search_issues)
builder.add_node("search_discussions", search_discussions)
builder.add_node("id_search_start", id_search_start)
builder.add_node("search_issues_by_id", search_issues_by_id)
builder.add_node("search_discussions_by_issue_id", search_discussions_by_issue_id)

builder.add_conditional_edges(
    START,
    route_by_input,
    {
        "search_issues": "search_issues",
        "id_search_start": "id_search_start"
    }
)
builder.add_edge("search_issues", "search_discussions")
builder.add_edge("search_discussions", END)

builder.add_edge("id_search_start", "search_issues_by_id")
builder.add_edge("id_search_start", "search_discussions_by_issue_id")
builder.add_edge("search_issues_by_id", END)
builder.add_edge("search_discussions_by_issue_id", END)

graph = builder.compile(checkpointer=MemorySaver())
graph.get_graph().print_ascii()

# --- 4. EXECUTION Test code ---
def test_one_run():
    inputs = {"query_keywords": "deployment data-export technical-debt identity-provider documentation"}
    # and handle the output properly.
    print("Running graph...")
    result = graph.ainvoke(inputs) 
    print(result)

def test_two_runs():
    inputs = {"query_keywords": "deployment data-export technical-debt identity-provider documentation"}
    # and handle the output properly.
    print("Running graph...")
    result = graph.ainvoke(inputs) 
    print(result)

    inputs = {"query_keywords": "network-topology"}
    # and handle the output properly.
    print("Running graph...")
    result = graph.ainvoke(inputs) 
    print(result)



# Logic to run the script
if __name__ == "__main__":
    test_one_run()
    test_two_runs()