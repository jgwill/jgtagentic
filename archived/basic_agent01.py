# See README.md for context

from langchain.agents import AgentExecutor, Tool
from langgraph.graph import StateGraph

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.checkpoint.
from langchain.chat_models.ollama import ChatOllama
from langchain.chat_models.openai import ChatOpenAI

# Define your tool functions
def tool_function(input_text):
    

# Define tools
