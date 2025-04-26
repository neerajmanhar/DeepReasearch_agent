from typing import Dict, List, Tuple, TypedDict, Annotated
from langgraph.graph import Graph, StateGraph
from agents.research_agent import ResearchAgent
from agents.answer_agent import AnswerAgent
import asyncio
from dotenv import load_dotenv

load_dotenv()

# Define the state schema
class AgentState(TypedDict):
    topic: str
    context: str
    research_results: List[Dict]
    current_answer: Dict
    iteration: int
    max_iterations: int
    search_type: str
    max_results: int
    max_tokens: int

# Initialize agents
research_agent = ResearchAgent()
answer_agent = AnswerAgent()

# Define the nodes
async def research_node(state: AgentState) -> AgentState:
    """
    Node for performing research
    """
    results, query = await research_agent.research_topic(
        topic=state["topic"],
        context=state["context"],
        max_iterations=1,  # Only one iteration
        search_type=state["search_type"],
        max_results=state["max_results"]
    )
    
    state["research_results"] = results
    state["iteration"] += 1
    return state

async def answer_node(state: AgentState) -> AgentState:
    """
    Node for generating answers
    """
    answer = await answer_agent.generate_answer(
        research_results=state["research_results"],
        query=state["topic"],
        additional_context=state["context"],
        max_tokens=state["max_tokens"]
    )
    
    state["current_answer"] = answer
    return state

# Create the graph
def create_research_graph() -> Graph:
    """
    Create the research workflow graph
    """
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("research", research_node)
    workflow.add_node("answer", answer_node)
    
    # Define the end node
    workflow.add_node("end", lambda x: x)
    
    # Add edges
    workflow.add_edge("research", "answer")
    workflow.add_edge("answer", "end")
    
    # Set entry point
    workflow.set_entry_point("research")
    
    return workflow.compile()

# Main function to run the research workflow
async def run_research_workflow(
    topic: str,
    context: str = "",
    max_iterations: int = 1,  # Set to 1 by default
    search_type: str = "basic",  # Default to basic search
    max_results: int = 2,  # Default to 2 results
    max_tokens: int = 256  # Default to 256 tokens
) -> Dict:
    """
    Run the complete research workflow
    """
    # Initialize the graph
    graph = create_research_graph()
    
    # Initialize the state
    initial_state: AgentState = {
        "topic": topic,
        "context": context,
        "research_results": [],
        "current_answer": {},
        "iteration": 0,
        "max_iterations": max_iterations,
        "search_type": search_type,
        "max_results": max_results,
        "max_tokens": max_tokens
    }
    
    # Run the graph
    final_state = await graph.ainvoke(initial_state)
    
    return final_state["current_answer"]

# Example usage
if __name__ == "__main__":
    async def main():
        result = await run_research_workflow(
            topic="What are the latest developments in quantum computing?",
            context="Focus on practical applications and industry adoption",
            max_iterations=1,
            search_type="basic",
            max_results=2,
            max_tokens=256
        )
        print("Final Answer:", result["content"])
        print("\nSources:")
        for source in result["sources"]:
            print(f"- {source['title']}: {source['url']}")
    
    asyncio.run(main()) 