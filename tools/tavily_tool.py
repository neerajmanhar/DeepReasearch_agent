from typing import Dict, List, Optional, Type, Any
from langchain.tools import BaseTool
from langchain.prompts import PromptTemplate
from tavily import TavilyClient
from pydantic import BaseModel, Field
import os


from dotenv import load_dotenv

load_dotenv()
TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY")
class TavilySearchInput(BaseModel):
    query: str = Field(..., description="The search query to execute")
    search_depth: str = Field(
        default="advanced",
        description="The depth of the search: 'basic' or 'advanced'"
    )
    max_results: int = Field(
        default=5,
        description="Maximum number of results to return"
    )

class TavilySearchTool(BaseTool):
    name: str = "tavily_search"
    description: str = """
    A powerful search tool that uses Tavily API to perform intelligent web searches.
    Input should be a search query string.
    The tool will return relevant web pages and their content.
    """
    args_schema: Type[BaseModel] = TavilySearchInput
    client: Any = Field(default=None, exclude=True)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
        
    def _run(self, query: str, search_depth: str = "advanced", max_results: int = 5) -> List[Dict]:
        """
        Execute the search using Tavily API
        """
        try:
            search_result = self.client.search(
                query=query,
                search_depth=search_depth,
                max_results=max_results
            )
            return search_result.get("results", [])
        except Exception as e:
            return [{"error": str(e)}]
    
    async def _arun(self, query: str, search_depth: str = "advanced", max_results: int = 5) -> List[Dict]:
        """
        Async implementation of the search
        """
        return self._run(query, search_depth, max_results)

# Advanced query generation prompt
QUERY_GENERATION_PROMPT = PromptTemplate(
    input_variables=["topic", "context"],
    template="""
    Given the research topic and context, generate an optimized search query.
    
    Topic: {topic}
    Context: {context}
    
    Generate a search query that will help find the most relevant and recent information.
    Focus on:
    1. Key concepts and terminology
    2. Recent developments or updates
    3. Expert opinions and analysis
    
    Search Query:
    """
) 