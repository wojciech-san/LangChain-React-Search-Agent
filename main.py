from dotenv import load_dotenv
import os
load_dotenv()

from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from tavily import TavilyClient

tavily = TavilyClient(api_key=os.environ.get("TAVILY_API_KEY"))

@tool
def search(query:str)-> str:
    """
    Tool that searches over internet
    Args:
        query: The query to seach for
    Returns:
        The search result
    """
    print(f"Searching for {query}")
    return tavily.search(query=query)

llm = ChatGoogleGenerativeAI(
        temperature=0,
        model="gemini-2.5-flash",
        api_key=os.environ.get("GOOGLE_API_KEY")  
)

tools = [search]
agent = create_agent(model=llm,tools=tools)

def main():
    print("Hello from langchain-react-search-agent!")
    result = agent.invoke({"messages":HumanMessage(content="What is the weather in Toyko?")})
    print(result)

if __name__ == "__main__":
    main()

 