from typing import List
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os
load_dotenv()

from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from tavily import TavilyClient
from langchain_tavily import TavilySearch

#tavily = TavilyClient(api_key=os.environ.get("TAVILY_API_KEY"))

# @tool
# def search(query:str)-> str:
#     """
#     Tool that searches over internet
#     Args:
#         query: The query to seach for
#     Returns:
#         The search result
#     """
#     print(f"Searching for {query}")
#     return tavily.search(query=query)


class Source(BaseModel):
    """Schema for a source used by the agent"""
    url: str = Field(description="The URL of the source")

class AgentResponse(BaseModel):
    """Schema for the response from the agent"""
    answer: str = Field(description="The agent's answer to the query")
    sources: List[Source] = Field(description="The sources used by the agent")    

llm = ChatGoogleGenerativeAI(
        temperature=0,
        model="gemini-2.5-flash",
        api_key=os.environ.get("GOOGLE_API_KEY")  
)

#tools = [search]
tools = [TavilySearch(api_key=os.environ.get("TAVILY_API_KEY"))] 
agent = create_agent(model=llm,tools=tools,response_format=AgentResponse)

content = "search for 3 job postings for an ai engineer using langchain in the bay area linkedin and list their details"

def main():
    print("Hello from langchain-react-search-agent!")
    result = agent.invoke({"messages":HumanMessage(content=content)})
    print(result)

if __name__ == "__main__":
    main()

 