from agent import graph

async def test_agent_simple_passthrough() -> None:
    inputs = {"changeme": "some_val"}
    res = await graph.ainvoke(inputs)
    return res
    

if __name__ == "__main__":
    import asyncio
    output = asyncio.run(test_agent_simple_passthrough())
    print(output)