from typing import Dict, List, Optional
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from utils.memory import ResearchMemory
import os
from datetime import datetime

from dotenv import load_dotenv
import json
from datetime import datetime

load_dotenv()

class AnswerAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.7
        )
        self.memory = ResearchMemory()
        self.current_date = datetime.now().strftime("%Y-%m-%d")
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", f"""
        You are an expert AI research assistant responsible for synthesizing search-based research into structured, factual, and clear responses.

        📅 Date: {self.current_date}

        Your responsibilities:
        1. Understand the user’s query and relevant context
        2. Use only the research results provided, avoiding hallucinations
        3. Emphasize recency when queries include phrases like “recent”, “latest”, “current”, or include dates
        4. Maintain a clear, factual, professional tone

        📌 Structure your response using the following format:
        - **Executive Summary**: A concise answer in 2–3 lines
        - **Key Findings**: Bullet points of main insights
        - **Detailed Analysis**: A deeper explanation with supporting facts
        - **Sources and Citations**: List of URLs or source names from research

        ⚠️ Never reference model knowledge or training cutoffs. Only use retrieved information and assume the current year is {self.current_date.split('-')[0]}.
        """),
            ("human", "{input}")
        ])

        
        
    async def generate_answer(self, 
                            research_results: List[Dict],
                            query: str,
                            additional_context: str = "",
                            max_tokens: int = 256) -> Dict:
        """
        Generate a comprehensive answer based on research results
        """
        answer_prompt = ChatPromptTemplate.from_messages([
            ("system", f"""
        You are an expert research analyst writing a comprehensive and up-to-date answer based on search results.

        📅 Date: {self.current_date}  
        Treat this as the current year for evaluating recency and relevance.

        ✅ Your Task:
        1. Analyze and synthesize the research findings carefully
        2. Prioritize recent and credible sources
        3. Structure the response clearly:
            - **Executive Summary** (short overview)
            - **Key Findings** (bullet points)
            - **Detailed Analysis** (well-organized, factual)
            - **Sources and Citations** (include links or names)

        🔎 Important Notes:
        - Respect terms like “recent”, “latest”, or any specific dates (e.g., April 2025) and adjust the temporal context accordingly.
        - Do NOT rely on outdated model knowledge or hallucinate details not found in the research.
        - Stay concise, factual, and avoid unnecessary verbosity.

        💡 Token Budget: Keep your output within {max_tokens} tokens.
        """),
            ("human", """Research Query: {query}
        Context: {context}

        Research Results:
        {research_results}

        Please draft a comprehensive, well-structured answer using the provided results.
        """)
        ])
                
        # Format the prompt with the actual values
        formatted_prompt = answer_prompt.format_messages(
            query=query,
            context=additional_context,
            research_results=self._format_research_results(research_results)
        )
        
        # Get answer from LLM
        response = await self.llm.ainvoke(formatted_prompt)
        
        # Extract sources from research results
        sources = self._extract_sources(research_results)
        
        return {
            "content": response.content,
            "sources": sources,
            "metadata": {
                "query": query,
                "timestamp": datetime.now().isoformat(),
                "source_count": len(sources),
                "max_tokens": max_tokens
            }
        }
    
    def _format_research_results(self, results: List[Dict]) -> str:
        """
        Format research results for the prompt
        """
        formatted = []
        for i, result in enumerate(results, 1):
            formatted.append(f"""
            Result {i}:
            Title: {result['title']}
            Content: {result['content']}
            Source: {result['source']}
            URL: {result['url']}
            """)
        return "\n".join(formatted)
    
    def _extract_sources(self, results: List[Dict]) -> List[Dict]:
        """Extract and clean sources from research results"""
        seen = set()
        sources = []
        for result in results:
            # Get URL from multiple possible fields
            url = result.get("url") or result.get("link") or ""
            if not url:
                continue
                
            # Clean title text
            title = result.get("title", "Source")
            if "for:" in title:
                title = title.split("for:")[0].strip()
            title = title.replace("Result for", "").strip()

            if url not in seen:
                seen.add(url)
                sources.append({
                    "title": title or "Source",
                    "url": url
                })
        return sources
    
    async def request_clarification(self, 
                                research_results: List[Dict],
                                query: str,
                                context: str = "") -> str:
        """
        Request clarification if the research results are insufficient
        """
        analysis_prompt = ChatPromptTemplate.from_messages([
            ("system", f"""
        You are an expert research analyst tasked with evaluating the sufficiency of search results to answer a user's query.

        📅 Date: {self.current_date}

        🧠 Your Job:
        1. Review the query, context, and research results
        2. Determine if the results are complete and relevant
        3. If not, clearly identify what information is missing
        4. Suggest 1–3 **precise and actionable** clarification questions that could improve the answer quality

        🚨 Focus on:
        - Gaps related to time-specific events (e.g., April 2025 attack, current laws, recent product launches)
        - Missing data points or comparative insights
        - Clarifications that help refine the search, not general prompts

        🎯 Be specific, practical, and concise.
        """),
            ("human", """Research Query: {query}
        Context: {context}

        Research Results:
        {research_results}

        Based on the above, what clarifications or follow-up questions would improve the research outcome?
        """)
        ])

        # Format the prompt with the actual values
        formatted_prompt = analysis_prompt.format_messages(
            query=query,
            context=context,
            research_results=json.dumps(research_results, indent=2)
        )
        # Get clarification request from LLM
        response = await self.llm.ainvoke(formatted_prompt)
        
        return response.content