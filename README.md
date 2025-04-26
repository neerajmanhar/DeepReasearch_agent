# Deep Research Agentic AI System

A powerful dual-agent system for automated deep research using LangChain, LangGraph, and Tavily API. This system combines intelligent web search capabilities with advanced natural language processing to produce comprehensive, well-structured research answers.

## Features

- 🤖 Dual-Agent Architecture
  - Research Agent: Performs intelligent web searches and information gathering
  - Answer Agent: Synthesizes information and generates comprehensive responses
- 🔄 Iterative Research Process
  - Multiple search passes with context-aware query generation
  - Automatic clarification requests when needed
- 💾 Persistent Memory
  - Stores research results for future reference
  - Enables knowledge retention across sessions
- 🎯 LangGraph Orchestration
  - Conditional workflow based on research quality
  - Flexible state management
  - Easy to extend and modify

## Prerequisites

- Python 3.9+
- Tavily API Key
- OpenAI API Key

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd deep-research-agent
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.template .env
```
Edit `.env` and add your API keys:
```
TAVILY_API_KEY=your_tavily_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
```

## Usage

### Basic Usage

```python
from main import run_research_workflow
import asyncio

async def main():
    result = await run_research_workflow(
        topic="What are the latest developments in quantum computing?",
        context="Focus on practical applications and industry adoption",
        max_iterations=3
    )
    print("Final Answer:", result["content"])
    print("\nSources:")
    for source in result["sources"]:
        print(f"- {source['title']}: {source['url']}")

asyncio.run(main())
```

### Advanced Usage

You can customize the research process by modifying the agents' behavior:

```python
from agents.research_agent import ResearchAgent
from agents.answer_agent import AnswerAgent

# Initialize agents with custom settings
research_agent = ResearchAgent()
answer_agent = AnswerAgent()

# Perform custom research
results = await research_agent.research_topic(
    topic="Your research topic",
    context="Additional context",
    max_iterations=5
)

# Generate custom answer
answer = await answer_agent.generate_answer(
    research_results=results,
    query="Your query",
    additional_context="More context"
)
```

## Project Structure

```
deep-research-agent/
├── agents/
│   ├── research_agent.py
│   └── answer_agent.py
├── tools/
│   └── tavily_tool.py
├── utils/
│   └── memory.py
├── main.py
 app.py
├── requirements.txt
├── .env
└── README.md
```


## Acknowledgments

- LangChain for the agent framework
- LangGraph for workflow orchestration
- Tavily for intelligent web search capabilities
- OpenAI for language model capabilities 