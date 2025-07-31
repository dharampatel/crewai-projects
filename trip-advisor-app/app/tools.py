from crewai.tools import tool
from langchain_community.tools import TavilySearchResults
import os
from dotenv import load_dotenv

load_dotenv()

search_tool = TavilySearchResults(tavily_api_key=os.getenv("TAVILY_API_KEY"), max_results=5)

@tool
def web_search_tool(query: str):
    """Search query on web and returns results."""
    return search_tool.invoke(query)

