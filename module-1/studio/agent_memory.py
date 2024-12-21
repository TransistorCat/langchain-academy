from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI

from langgraph.graph import START, StateGraph, MessagesState
from langgraph.prebuilt import tools_condition, ToolNode
from dotenv import load_dotenv
import os
from pprint import pprint
from langchain_core.messages import AIMessage, HumanMessage
# 加载 .env 文件
load_dotenv()
def add(a: int, b: int) -> int:
    """Adds a and b.

    Args:
        a: first int
        b: second int
    """
    return a + b

def multiply(a: int, b: int) -> int:
    """Multiplies a and b.

    Args:
        a: first int
        b: second int
    """
    return a * b

def divide(a: int, b: int) -> float:
    """Divide a and b.

    Args:
        a: first int
        b: second int
    """
    return a / b

tools = [add, multiply, divide]

# Define LLM with bound tools
llm = ChatOpenAI(model=os.environ["LLM_MODELEND"], temperature=0)
llm_with_tools = llm.bind_tools(tools)

# System message
sys_msg = SystemMessage(content="You are a helpful assistant tasked with writing performing arithmetic on a set of inputs.")

# Node
def assistant(state: MessagesState):
   return {"messages": [llm_with_tools.invoke([sys_msg] + state["messages"])]}

# Build graph
builder = StateGraph(MessagesState)
builder.add_node("assistant", assistant)
builder.add_node("tools", ToolNode(tools))
builder.add_edge(START, "assistant")
builder.add_conditional_edges(
    "assistant",
    # If the latest message (result) from assistant is a tool call -> tools_condition routes to tools
    # If the latest message (result) from assistant is a not a tool call -> tools_condition routes to END
    tools_condition,
)
builder.add_edge("tools", "assistant")

# Compile graph
graph = builder.compile()




if __name__ == "__main__":

    from langgraph.checkpoint.memory import MemorySaver

    memory=MemorySaver()
    react_graph_memory = builder.compile(checkpointer=memory)
    # Specify a thread
    config = {"configurable": {"thread_id": "1"}}

    # Specify an input
    messages = [HumanMessage(content="Add 3 and 4.")]

    # Run
    messages = react_graph_memory.invoke({"messages": messages},config)
    for m in messages['messages']:
        m.pretty_print()

    messages = [HumanMessage(content="Multiply that by 2.")]
    messages = react_graph_memory.invoke({"messages": messages}, config)
    for m in messages['messages']:
        m.pretty_print()