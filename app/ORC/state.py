from typing import Dict, TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage,SystemMessage
from langgraph.graph import StateGraph, START, END, add_messages
from langgraph.prebuilt import ToolNode
from langchain_core.messages import HumanMessage, AIMessage
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from app.core.config import settings
from IPython.display import Image, display
from app.RAG.RAG_Agent import answer
from app.Agents.ops.tools import check_table_availability, book_table, cancel_booking

tools=[answer, check_table_availability, book_table, cancel_booking]
llm=ChatGroq(model="openai/gpt-oss-120b",api_key=settings.GROQ_API_KEY).bind_tools(tools) 

class Agent_state(TypedDict):
  messages: Annotated[Sequence[BaseMessage],add_messages]
  conversation_id: str
  user_id: str
def model(state: Agent_state) -> Agent_state:
  """The brain"""
  sys_prompt=SystemMessage(content='''You are a helpful AI assistant for serving clients in Yahya_Restaurant.

You have access to some tools: RAG Agent, check_table_availability, book_table, cancel_booking.

You need to decide which tool to use based on the user's question.
If the question is about the restaurant's menu, prices, ingredients, opening hours, or policies, use the RAG Agent tool to answer it.
If the question is about checking table availability, use the check_table_availability tool.
If the question is about booking a table, use the book_table tool.
If the question is about canceling a booking, use the cancel_booking tool.
Do not answer questions about the restaurant's menu, prices, ingredients, opening hours, or policies yourself. Instead, use the RAG Agent tool to answer them.

When the client requests a multiple requests, execute each one in the order they are given if they didn't specify the order, excute in a reasonable order. If the client requests a single request, execute it.

After all requests are complete, provide the final answer.''')
  response=llm.invoke([sys_prompt]+state["messages"])
  return {"messages":[response]}
def decision(state:Agent_state) -> str:
  messages=state["messages"]
  last_message=messages[-1]
  if not last_message.tool_calls:
    return 'end'
  elif last_message.tool_calls:
    return 'tools'
graph=StateGraph(Agent_state)
graph.add_node('Groq',model)
tool_node=ToolNode(tools=tools)
graph.add_node('tool',tool_node)
graph.add_edge(START,'Groq')
graph.add_conditional_edges(
    'Groq',
    decision,
    {'tools':'tool','end':END}
)
graph.add_edge('tool','Groq')
app=graph.compile()
'''graph = app.get_graph()

png_data = graph.draw_mermaid_png()

with open("graph.png", "wb") as f:
    f.write(png_data)
'''
def print_stream(stream):
    for s in stream:
        message = s["messages"][-1]
        if isinstance(message, tuple):
            print(message)
        else:
            message.pretty_print()
input={'messages':[('user','My name is yahya... I want to eat beaf do you have meals containing beef and then i want to book a table in Cairo branch at 2026-9-25 at 20:00.')]}

print_stream(app.stream(input, stream_mode='values'))