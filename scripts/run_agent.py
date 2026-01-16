from agent import graph

async def test_agent_simple_passthrough() -> None:
    inputs = {"changeme": "some_val"}
    res = await graph.ainvoke(inputs)
    assert res is not None

if __name__ == "__main__":
    test_agent_simple_passthrough()