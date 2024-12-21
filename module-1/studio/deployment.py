import asyncio
from langgraph_sdk import get_client
from langchain_core.messages import HumanMessage

# Replace this with the URL of your own deployed graph
URL = "http://localhost:2024"
client = get_client(url=URL)

# async def main():
#     # Search all hosted graphs
#     assistants = await client.assistants.search()

#     # We create a thread for tracking the state of our run
#     thread = await client.threads.create()

#     # Input
#     input = {"messages": [HumanMessage(content="Multiply 3 by 2.")]}

#     # Stream
#     async for chunk in client.runs.stream(
#             thread['thread_id'],
#             "agent",
#             input=input,
#             stream_mode="values",
#         ):
#         if chunk.data and chunk.event != "metadata":
#             print(chunk.data['messages'][-1])

# # Run the main function
# asyncio.run(main())


def main():
    # Search all hosted graphs
    assistants = client.assistants.search()

    # We create a thread for tracking the state of our run
    thread = client.threads.create()

    # Input
    input = {"messages": [HumanMessage(content="Multiply 3 by 2.")]}

    # Stream
    for chunk in client.runs.stream(
            thread['thread_id'],
            "agent",
            input=input,
            stream_mode="values",
        ):
        if chunk.data and chunk.event != "metadata":
            print(chunk.data['messages'][-1])

# Run the main function
main()