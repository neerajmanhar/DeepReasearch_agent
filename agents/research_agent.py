from typing import List, Dict, Tuple
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from tools.tavily_tool import TavilySearchTool
import os
from dotenv import load_dotenv
from datetime import datetime
load_dotenv()

class ResearchAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.7
        )
        self.tavily = TavilySearchTool()
        self.current_date = datetime.now().strftime("%Y-%m-%d")
        self.prompt = ChatPromptTemplate.from_messages([
        ("system", f"""
    You are an intelligent, up-to-date research assistant who crafts high-quality search engine queries to help find the most recent and reliable information from the web.

    📅 Date: {self.current_date}  
    Ignore any outdated training knowledge. Instead, focus on helping the user find real-time, factual answers through smart search queries.

    🔍 How to Write the Best Query:
    1. If the user mentions “recent”, “latest”, “today”, or specific dates (e.g., April 2025), **explicitly include those in the search**.
    2. If the topic relates to **news, politics, current events, or tech updates**, focus on real-world developments post-2023.
    3. If no time reference is provided, **default to searching for updates from the past 1–2 years**.
    4. Your output should be a single, effective, search-friendly query.

    🛠️ Examples:
    - Good: `India response to Pahalgam April 2025 terrorist attack civilians treaty cancelled`
    - Good: `Firebase Studio vs Cursor AI vs other app building tools 2024 2025 updates`
    - Avoid vague or general queries.

    🎯 Output:
    - Return **only the final search query**, ready to be passed to Tavily.
    - Do not include extra text, explanations, or formatting.
    """),
        ("human", """
    Research Topic: {topic}
    Additional Context: {context}

    Write one optimized search query based on this information:
    """)
    ])

    async def research_topic(
        self,
        topic: str,
        context: str = "",
        max_iterations: int = 1,
        search_type: str = "basic",
        max_results: int = 2
    ) -> Tuple[List[Dict], str]:
        # Generate research query with length constraint
        response = await self.llm.ainvoke(
            self.prompt.format(topic=topic, context=context)
        )
        query = response.content[:380].strip() + "..."  # Enforce 380 char limit
        
        try:
            # Get Tavily results with error handling
            raw_results = await self.tavily._arun(
                query=query,
                search_depth=search_type,
                max_results=max_results
            )
        except Exception as e:
            print(f"Tavily Error: {str(e)}")
            return [{"error": str(e)}], query
        
        # Process results with validation
        results = []
        for res in raw_results:
            if 'error' in res:
                continue  # Skip error entries
                
            result = {
                "title": res.get("title", "No title").split("for:")[0].strip(),
                "content": res.get("content", ""),
                "url": res.get("url") or res.get("link", ""),
                "source": "Tavily",
                "timestamp": str(res.get("timestamp", ""))
            }
            
            # Validate URL format
            if result["url"].startswith(("http://", "https://")):
                results.append(result)
        
        print("Processed Results:", results)  # Debug cleaned results
        return results, query