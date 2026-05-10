from searchlib.search_engine import IssueSearchEngine

# Test for IssueSearchEngine async search functionality
import asyncio

def test_issue_search_engine():
    engine = IssueSearchEngine()

    # Test single keyword search
    results = asyncio.run(engine.asearch("rollback"))
    assert len(results) == 1
    assert results[0]['issue_id'] == "LL-1001"

    # Test multiple keywords search
    results = asyncio.run(engine.asearch(["deployment", "audit"]))
    assert len(results) == 6

    # Test keyword with no matches
    results = asyncio.run(engine.asearch("non-existent-keyword"))
    assert len(results) == 0

