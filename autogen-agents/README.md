# AutoGen Financial News Aggregation System

## Project Overview
This project implements an automated financial news aggregation and article writing system using Microsoft's AutoGen framework. The system coordinates multiple AI agents to gather, analyze, and produce financial articles by combining news from different sources.

## Architecture Design

### Core Agents
1. **Planner Agent**
   - Orchestrates the overall workflow
   - Assigns tasks to other agents
   - Determines article topics and priorities
   - Ensures coherent information flow

2. **Google News Agent**
   - Fetches financial news from Google News
   - Filters relevant financial information
   - Extracts key data points and trends
   - Provides primary market news coverage

3. **Yahoo Finance Agent**
   - Retrieves stock market data and shock events
   - Monitors market movements and trading signals
   - Captures breaking financial news
   - Analyzes stock performance metrics

4. **Financial Writer Agent**
   - Synthesizes information from other agents
   - Produces coherent financial articles
   - Ensures accurate financial terminology
   - Maintains consistent writing style

### Communication Flow
```
                [Planner Agent]
                      ↓
    ┌─────────────────┴─────────────────┐
    ↓                 ↓                 ↓
[Google News]  [Yahoo Finance]  [Financial Writer]
    │                 │                 ↑
    └─────────────────┴─────────────────┘
```

## Components Description

### 1. Agent Implementations (`src/agents/`)
- `planner_agent.py`: Workflow orchestration and task management
- `google_news_agent.py`: Google News data fetching and processing
- `yahoo_finance_agent.py`: Yahoo Finance integration and stock analysis
- `writer_agent.py`: Article generation and formatting

### 2. Core Modules (`src/`)
- `manager/`: Agent coordination and lifecycle management
- `utils/`: 
  - News processing utilities
  - Financial data handlers
  - Text processing tools
- `communication/`: Inter-agent message routing

### 3. Configuration (`config/`)
- API credentials for news sources
- Agent behavior parameters
- Output formatting settings
- Communication protocols

### 4. Examples (`examples/`)
- Sample article generation workflows
- News aggregation examples
- Multi-source analysis demonstrations

## Setup Instructions
1. Create a Python virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install required dependencies
```bash
pip install autogen requests beautifulsoup4 yfinance
```

3. Configure API credentials
- Set up Google News API access
- Configure Yahoo Finance API credentials
- Set up any additional required APIs

4. Initialize the system
```bash
python src/main.py
```

## Project Structure
```
autogen-agents/
├── src/
│   ├── agents/
│   │   ├── planner_agent.py
│   │   ├── google_news_agent.py
│   │   ├── yahoo_finance_agent.py
│   │   └── writer_agent.py
│   ├── manager/
│   │   └── agent_manager.py
│   ├── utils/
│   │   ├── news_processor.py
│   │   ├── financial_utils.py
│   │   └── text_processor.py
│   └── communication/
│       └── message_broker.py
├── config/
│   ├── api_config.json
│   └── agent_config.json
├── examples/
│   └── sample_workflow.py
├── tests/
│   └── test_agents.py
└── README.md
```

## Future Enhancements
1. Add support for additional news sources
2. Implement sentiment analysis
3. Add market prediction capabilities
4. Enhance article generation with templates
5. Add real-time news monitoring
6. Implement automated publishing workflow

## Requirements
- Python 3.8+
- AutoGen framework
- Google News API access
- Yahoo Finance API access
- Additional dependencies (specified in requirements.txt)

## License
MIT License

Note: This is an initial design document that outlines the financial news aggregation system. Implementation details and additional features can be added based on specific requirements.