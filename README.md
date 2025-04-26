# Deep Research Agentic AI System

A powerful dual-agent system for automated deep research using LangChain, LangGraph, and the Tavily API. This system autonomously gathers real-time information and synthesizes structured, source-cited answers based on user queries.

## Features
- **Dual-Agent Architecture**  
  - **Research Agent**: Crafts high-quality, time-aware search queries and collects reliable, current web data.
  - **Answer Agent**: Synthesizes and structures the search results into a professional, fact-based answer.
- **Iterative Research Process**  
  - Implements conditional workflows (via LangGraph) to re-query or ask clarifying questions when results are insufficient.
- **Persistent Memory**  
  - Integrates with ChromaDB for storing and retrieving research data across sessions.
- **Interactive Web App**  
  - Deployed using Streamlit for an intuitive, real-time research interface.

## Prerequisites
- API Keys for Tavily and OpenAI

## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/neerajmanhar/DeepReasearch_agent
   cd deep-research-agent
   ```

2. **Create and Activate a Virtual Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

   ```bash
   # conda version
   conda create --name venv
   conda activate venv

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables:**
   Create a `.env` file and add your API keys:
   ```env
   TAVILY_API_KEY=your_tavily_api_key_here
   OPENAI_API_KEY=your_openai_api_key_here
   CHROMA_PERSIST_DIR=./data/chroma
   ```

## Usage

### Running the Research Workflow

You can run the research workflow via the command line:
```bash
python main.py
```

### Starting the Streamlit App

To launch the interactive web interface:
```bash
streamlit run app.py
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
├── app.py
├── README.md
├── requirements.txt
├── .env
```

## Implementation Overview

### Research Agent
- **Query Generation:** Uses GPT-4o-mini to generate precise, time-aware search queries.
- **Data Collection:** Connects with the Tavily API to retrieve web search results, filtering and processing to ensure valid URLs and up-to-date data.

### Answer Agent
- **Synthesis & Structure:** Analyzes the research data to produce a well-organized answer with an executive summary, key findings, detailed analysis, and comprehensive citations.
- **Clarification:** In case of insufficient data, it suggests precise follow-up questions to refine the search.

### Workflow Orchestration
- **LangGraph Based Execution:** Manages the research and answer generation stages as nodes in a directed graph, allowing conditional routing and iterative clarification.

### Memory Integration
- **ChromaDB:** Stores and retrieves research results, supporting persistent knowledge across research sessions.

