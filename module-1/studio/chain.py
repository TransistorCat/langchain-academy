from langchain_openai import ChatOpenAI
from langgraph.graph import MessagesState
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from dotenv import load_dotenv
import os
from pprint import pprint
from langchain_core.messages import AIMessage, HumanMessage

# 加载 .env 文件
load_dotenv()

# Tool
def multiply(a: int, b: int) -> str:
    """Multiplies a and b and returns the result as a string."""
    return str(a * b)

# LLM with bound tool
llm = ChatOpenAI(model=os.environ["LLM_MODELEND"], temperature=0)
llm_with_tools = llm.bind_tools([multiply])

# Node
def tool_calling_llm(state: MessagesState):
    # 获取当前消息状态并调用工具
    print("当前状态:", state)
    messages = state["messages"]
    print("当前messages:", messages)
    response = llm_with_tools.invoke(messages)
    print("工具响应:", response)
    # 返回工具的响应，确保格式正确
    return {"messages": response}
# Build graph
builder = StateGraph(MessagesState)
builder.add_node("tool_calling_llm", tool_calling_llm)
builder.add_edge(START, "tool_calling_llm")
builder.add_edge("tool_calling_llm", END)
# Compile graph
graph = builder.compile()

if __name__ == "__main__":
    messages = graph.invoke({"messages": HumanMessage(content="Multiply 2 and 3")})
    for m in messages['messages']:
        m.pretty_print()
    messages = graph.invoke({"messages": HumanMessage(content="who are you?")})
    for m in messages['messages']:
        m.pretty_print()


        